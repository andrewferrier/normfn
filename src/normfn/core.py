import datetime
import logging
import sys
from contextlib import suppress
from io import TextIOBase
from pathlib import Path

from normfn.args import Args, parse_arguments
from normfn.dates import YearRegexes, datetime_prefix
from normfn.exceptions import FatalError, _QuitSignalError
from normfn.files import (
    ask_yes_no,
    rlinput,
    shiftfile,
    should_exclude,
    validate_move,
)

if not sys.version_info >= (3, 12):
    msg = "Needs at least Python 3.12"  # pyright: ignore[reportUnreachable]
    raise ValueError(msg)


def main(argv: list[str], syserr_handler: logging.StreamHandler[TextIOBase]) -> None:
    logger = logging.getLogger("normfn")

    args = parse_arguments(argv)

    if syserr_handler:
        if args.verbose > 1:
            syserr_handler.setLevel(logging.DEBUG)
        elif args.verbose == 1:
            syserr_handler.setLevel(logging.INFO)
        else:
            syserr_handler.setLevel(logging.WARNING)

    logger.debug(f"Arguments are: {args}")

    year_now = datetime.datetime.now(tz=datetime.UTC).year
    year_range_list = [
        str(year)
        for year in range(
            year_now - args.max_years_behind, year_now + args.max_years_ahead
        )
    ]

    two_digit_years: list[str] = [year_str[-2:] for year_str in year_range_list]
    two_to_four_digit_year_map: dict[str, str] = {
        year_str[-2:]: year_str for year_str in year_range_list
    }

    year_regexes = YearRegexes(
        four_digit_year_regex=r"(" + "|".join(year_range_list) + r")",
        all_digit_year_regex=r"(" + "|".join(year_range_list + two_digit_years) + r")",
        two_to_four_digit_year_map=two_to_four_digit_year_map,
    )

    with suppress(_QuitSignalError):
        for arg_filename in args.filenames:
            filename = arg_filename.resolve()
            if not filename.exists():
                msg = f"{filename} specified on the command line does not exist."
                raise FatalError(msg)

            if filename.is_dir() and args.recursive:
                new_filename = process_filename(filename, args, year_regexes)
                walk_tree(new_filename, args, year_regexes)
            else:
                process_filename(filename, args, year_regexes)


def walk_tree(dirname: Path, args: Args, year_regexes: YearRegexes) -> None:
    logger = logging.getLogger("normfn")

    logger.debug(f"Walking directory tree {dirname}")
    dirlist: list[Path] = sorted(Path(dirname).iterdir())

    for entry in dirlist:
        entry_full = dirname / entry

        entry_full = process_filename(entry_full, args, year_regexes)
        if entry_full.is_dir():
            walk_tree(entry_full, args, year_regexes)


def process_filename(
    original_path: Path, args: Args, year_regexes: YearRegexes
) -> Path:
    logger = logging.getLogger("normfn")

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

    validate_move(args.force, original_path, target_path)

    if move_it:
        if not args.dry_run:
            shiftfile(args.undo_log_file, original_path, target_path)
            return target_path

        logger.info(
            f"Not moving {str(original_path).strip()} to {target_path}; dry run."
        )
        return original_path

    logger.info(f"Not moving {str(original_path).strip()}")
    return original_path
