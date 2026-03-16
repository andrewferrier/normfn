import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from typing import Any, Literal, NoReturn, cast, override

from normfn.exceptions import FatalError
from normfn.files import get_default_log_file


@dataclass
class Args:
    verbose: int
    help: bool
    version: bool
    dry_run: bool
    interactive: bool
    all: bool
    force: bool
    add_time: bool
    discard_existing_name: bool
    recursive: bool
    max_years_ahead: int
    max_years_behind: int
    undo_log_file: Path | None
    no_undo_log_file: bool
    time_option: Literal["now", "earliest", "latest"]
    filenames: list[Path]


def parse_arguments(argv: list[str]) -> Args:
    class ArgumentParser(argparse.ArgumentParser):
        @override
        def error(self, message: str) -> NoReturn:
            parser.print_help()
            raise FatalError(message)

    parser = ArgumentParser(
        description=(
            "Normalizes filenames by prefixing a date to them. "
            "See https://github.com/andrewferrier/normfn for more information."
        ),
        add_help=False,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Add debugging output. Using this twice makes it doubly verbose.",
    )

    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        help="Show help information for normfn.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Show the version of normfn and exit.",
    )

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help=(
            "Don't actually make any changes, just show them. Forces "
            "a single level of verbosity (-v)."
        ),
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        dest="interactive",
        help="Ask about each change before it is done.",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all",
        help="Affect all files, including those in default exclude lists.",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help=(
            "Overwrite target files if they already exist "
            "(USE WITH CAUTION, consider using --dry-run first)."
        ),
    )

    parser.add_argument(
        "-t",
        "--add-time",
        action="store_true",
        dest="add_time",
        help="If a time is not found in the filename, add one.",
    )

    parser.add_argument(
        "-d",
        "--discard-existing-name",
        action="store_true",
        dest="discard_existing_name",
        help="Discard existing name and just use the date/time prefix.",
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        dest="recursive",
        default=False,
        help=(
            "Recurse into directories specified on the command line. The default is "
            "not to do this, and simply look at the name of the directory itself."
        ),
    )

    parser.add_argument(
        "--max-years-ahead",
        type=int,
        dest="max_years_ahead",
        default=5,
        help=(
            "Consider years further ahead from now than this not "
            "to be valid years. Defaults to 5."
        ),
    )

    parser.add_argument(
        "--max-years-behind",
        type=int,
        dest="max_years_behind",
        default=30,
        help=(
            "Consider years further behind from now than this not "
            "to be valid years. Defaults to 30."
        ),
    )

    log_option = parser.add_mutually_exclusive_group()

    log_option.add_argument(
        "--undo-log-file",
        type=Path,
        dest="undo_log_file",
        help=(
            "The name of the shell script to log "
            "'undo commands' for normfn; see the "
            "instructions in the file to use. "
            f"Defaults to {get_default_log_file()}"
        ),
    )

    log_option.add_argument(
        "--no-undo-log-file",
        dest="no_undo_log_file",
        action="store_true",
        help="Inverse of --undo-log-file; don't store undo commands.",
    )

    time_option = parser.add_mutually_exclusive_group()

    time_option.add_argument(
        "--now",
        action="store_const",
        dest="time_option",
        const="now",
        help=(
            "Use date and time now as the default "
            "file prefix for filenames without them."
        ),
    )

    time_option.add_argument(
        "--latest",
        "--newest",
        action="store_const",
        dest="time_option",
        const="latest",
        help=(
            "Use the latest of ctime and mtime "
            "to define a file prefix for files without them. "
            "Note: ctime is *not* "
            "file creation on Linux/OS X; see "
            "http://lwn.net/Articles/397442/."
        ),
    )

    time_option.add_argument(
        "--earliest",
        "--oldest",
        action="store_const",
        dest="time_option",
        const="earliest",
        help=(
            "Use earliest of ctime and mtime "
            "to define a file prefix for files without them. "
            "This is the default."
        ),
    )

    parser.set_defaults(
        time_option="earliest",
        undo_log_file=get_default_log_file(),
    )

    class FilenamesAction(argparse.Action):
        @override
        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: str | Sequence[Any] | None,
            option_string: str | None = None,
        ) -> None:
            typed_values = cast("Sequence[Path]", values)
            namespace.filenames = list(typed_values)
            args_help: bool = namespace.help  # pyright: ignore[reportAny]
            args_version: bool = namespace.version  # pyright: ignore[reportAny]
            if not args_help and not args_version and len(typed_values) < 1:
                parser.error("You must specify some file or directory names.")

    parser.add_argument(
        "filenames",
        type=Path,
        metavar="filename",
        nargs="*",
        help="Filenames",
        action=FilenamesAction,
    )

    args_ns = parser.parse_args(argv[1:])

    args = Args(**vars(args_ns))  # pyright: ignore[reportAny]

    if args.help:
        parser.print_help()
        sys.exit(0)

    if args.version:
        print(version("normfn"))  # noqa: T201
        sys.exit(0)

    return args
