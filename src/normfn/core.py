import logging
import sys
from contextlib import suppress
from io import TextIOBase
from pathlib import Path

from normfn.args import Args, parse_arguments
from normfn.config import (
    create_template_config,
    get_default_config_path,
    load_config,
    resolve_undo_log_file,
)
from normfn.dates import YearRegexes, datetime_prefix, make_year_regexes
from normfn.exceptions import FatalError, _QuitSignalError
from normfn.files import shiftfile, should_exclude
from normfn.input import ask_yes_no, rlinput

if not sys.version_info >= (3, 12):
    msg = "Needs at least Python 3.12"  # pyright: ignore[reportUnreachable]
    raise ValueError(msg)

logger = logging.getLogger(__name__)


def main(argv: list[str], syserr_handler: logging.StreamHandler[TextIOBase]) -> None:
    args = parse_arguments(argv)

    if syserr_handler:
        if args.verbose > 1:
            syserr_handler.setLevel(logging.DEBUG)
        elif args.verbose == 1:
            syserr_handler.setLevel(logging.INFO)
        else:
            syserr_handler.setLevel(logging.WARNING)

    if args.initialize_config:
        config_path = args.config or get_default_config_path()
        if config_path.exists():
            msg = (
                f"Config file already exists: {config_path}. "
                "Remove it first if you want to regenerate it."
            )
            raise FatalError(msg)
        create_template_config(config_path)
        print(f"Created config file: {config_path}")  # noqa: T201
        return

    config = load_config(args.config)

    logger.debug(f"Arguments are: {args}")
    logger.debug(f"Config is: {config}")

    year_regexes = make_year_regexes(config.max_years_behind, config.max_years_ahead)
    undo_log_file = resolve_undo_log_file(config)

    with suppress(_QuitSignalError):
        for arg_filename in args.filenames:
            filename = arg_filename.resolve()
            if not filename.exists():
                msg = f"{filename} specified on the command line does not exist."
                raise FatalError(msg)

            if filename.is_dir() and args.recursive:
                new_filename = process_filename(
                    filename, args, year_regexes, undo_log_file
                )
                walk_tree(new_filename, args, year_regexes, undo_log_file)
            else:
                process_filename(filename, args, year_regexes, undo_log_file)


def walk_tree(
    dirname: Path,
    args: Args,
    year_regexes: YearRegexes,
    undo_log_file: Path | None,
) -> None:
    logger.debug(f"Walking directory tree {dirname}")
    dirlist: list[Path] = sorted(Path(dirname).iterdir())

    for entry in dirlist:
        entry_full = dirname / entry

        entry_full = process_filename(entry_full, args, year_regexes, undo_log_file)
        if entry_full.is_dir():
            walk_tree(entry_full, args, year_regexes, undo_log_file)


def process_filename(
    original_path: Path,
    args: Args,
    year_regexes: YearRegexes,
    undo_log_file: Path | None,
) -> Path:
    logger.debug(f"Processing filename {original_path}")

    if not args.all:
        (exclude, why) = should_exclude(str(original_path), original_path.name)
        if exclude:
            logger.info(
                f"Skipping {str(original_path).strip()} as it matches pattern {why}"
            )
            return original_path

    new_stem = datetime_prefix(args, original_path.stem, original_path, year_regexes)
    new_stem = new_stem.strip() + original_path.suffix
    target_path = original_path.parent / new_stem

    logger.debug(f"Potential new filename for {original_path} is {target_path}")

    if target_path == original_path:
        logger.debug("New filename would be identical, skipping.")
        return original_path

    move_it = True

    if args.interactive:
        move_it_choice = ask_yes_no(
            f"Move {str(original_path).strip()} to .../{new_stem} [y/n/e/q]?"
        )
        if move_it_choice == b"e":
            edited_basename = rlinput("What new filename? ", new_stem)
            target_path = original_path.parent / edited_basename
        else:
            move_it = move_it_choice == b"y"

    if target_path.exists() and not args.force:
        raise FatalError(
            f"Want to move {original_path} to "
            + f"{target_path}, but it already exists."
        )

    if move_it:
        if not args.dry_run:
            shiftfile(undo_log_file, original_path, target_path)
            return target_path

        logger.info(
            f"Not moving {str(original_path).strip()} to {target_path}; dry run."
        )
        return original_path

    logger.info(f"Not moving {str(original_path).strip()}")
    return original_path
