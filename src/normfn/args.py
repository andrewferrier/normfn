import argparse
import dataclasses
import os
import sys
from collections.abc import Sequence
from importlib.metadata import version
from pathlib import Path
from typing import Any, Literal, NoReturn, cast, override

import shtab

from normfn.config import get_default_config_path
from normfn.exceptions import FatalError


def _detect_shell() -> str:
    shell_path = os.environ.get("SHELL", "")
    shell_name = Path(shell_path).name if shell_path else ""
    supported: list[str] = shtab.SUPPORTED_SHELLS
    return shell_name if shell_name in supported else supported[0]


@dataclasses.dataclass
class Args:
    verbose: int
    help: bool
    version: bool
    config: Path | None
    initialize_config: bool
    dry_run: bool
    interactive: bool
    all: bool
    force: bool
    add_time: bool
    discard_existing_name: bool
    recursive: bool
    time_option: Literal["now", "earliest", "latest"]
    filenames: list[Path]


def get_parser() -> argparse.ArgumentParser:
    class ArgumentParser(argparse.ArgumentParser):
        @override
        def error(self, message: str) -> NoReturn:
            parser.print_help()
            raise FatalError(message)

    parser = ArgumentParser(
        prog="normfn",
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
        "--config",
        type=Path,
        default=None,
        metavar="PATH",
        help=(
            f"Path to the configuration file. Defaults to {get_default_config_path()}."
        ),
    )

    # I considered and investigating having this conflict with other options
    # but it's just too much maintenance headache. Long-term approach should
    # maybe be to refactor to subcommands.
    parser.add_argument(
        "--initialize-config",
        action="store_true",
        dest="initialize_config",
        help=(
            "Create a template configuration file at the path given by --config "
            f"(default: {get_default_config_path()}) and exit. "
            "Fails if the file already exists."
        ),
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
            "file creation on Linux/macOS; see "
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
        time_option=None,
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
            if (
                not namespace.help
                and not namespace.version
                and not namespace.initialize_config
                and len(typed_values) < 1
            ):
                parser.error("You must specify some file or directory names.")

    parser.add_argument(
        "filenames",
        type=Path,
        metavar="filename",
        nargs="*",
        help="Filenames",
        action=FilenamesAction,
    )

    class CompletionsAction(argparse.Action):
        @override
        def __call__(
            self,
            _parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: str | Sequence[Any] | None,
            option_string: str | None = None,
        ) -> None:
            shell = str(values) if values is not None else _detect_shell()
            print(shtab.complete(parser, shell=shell))  # noqa: T201
            sys.exit(0)

    parser.add_argument(
        "--completions",
        nargs="?",
        const=None,
        default=argparse.SUPPRESS,
        choices=shtab.SUPPORTED_SHELLS,
        metavar="{" + ",".join(shtab.SUPPORTED_SHELLS) + "}",
        action=CompletionsAction,
        help=(
            "Output a shell completion script, then exit. "
            "Shell is auto-detected from $SHELL if not specified."
        ),
    )

    return parser


def parse_arguments(argv: list[str]) -> Args:
    parser = get_parser()

    args_ns = parser.parse_args(argv[1:])

    if args_ns.time_option is None:
        args_ns.time_option = "earliest"

    _args_fields = {f.name for f in dataclasses.fields(Args)}
    args = Args(**{k: v for k, v in vars(args_ns).items() if k in _args_fields})

    if args.help:
        parser.print_help()
        sys.exit(0)

    if args.version:
        print(version("normfn"))  # noqa: T201
        sys.exit(0)

    if args.dry_run:
        args.verbose = max(args.verbose, 1)

    return args
