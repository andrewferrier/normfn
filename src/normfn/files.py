import datetime
import logging
import os
import re
import shlex
import shutil
import sys
import textwrap
from io import TextIOBase
from pathlib import Path
from re import Pattern
from typing import Literal, cast

from normfn.exceptions import FatalError, _QuitSignal

EFFECTIVE_SEP: str = r"\\" if os.sep == "\\" else os.sep

BASENAME_EXCLUDE_PATTERNS: frozenset[Pattern] = frozenset(
    [re.compile(r"\..*"), re.compile("Icon\r"), re.compile(r".*\.lo?ck")]
)

FULLNAME_EXCLUDE_PATTERNS: frozenset[Pattern] = frozenset(
    [
        re.compile(r".*\.git" + EFFECTIVE_SEP + r".*"),
        re.compile(r".*\.svn" + EFFECTIVE_SEP + r".*"),
        re.compile(r".*\.hg" + EFFECTIVE_SEP + r".*"),
        re.compile(r".*\.bzr" + EFFECTIVE_SEP + r".*"),
    ]
)


def get_default_log_file() -> Path:
    home: Path = Path("~").expanduser()
    xdg_state_home: Path = Path(
        os.environ.get("XDG_STATE_HOME") or home / ".local" / "state"
    )
    return xdg_state_home / "normfn-undo.log.sh"


def should_exclude(filename: str, basename: str) -> tuple[bool, Pattern | None]:
    match = False
    exclude_pattern: Pattern | None = None

    for current_pattern in BASENAME_EXCLUDE_PATTERNS:
        if re.fullmatch(current_pattern, basename):
            match = True
            exclude_pattern = current_pattern
            break

    if not match:
        for current_pattern in FULLNAME_EXCLUDE_PATTERNS:
            if re.fullmatch(current_pattern, filename):
                match = True
                exclude_pattern = current_pattern
                break

    return (match, exclude_pattern)


def get_pdf_creation_date(filename: Path) -> datetime.datetime | None:
    logger = logging.getLogger("normfn")

    if filename.suffix.lower() != ".pdf":
        return None

    try:
        import pypdf  # noqa: PLC0415
    except ImportError:
        logger.info("pypdf library not available; cannot read PDF creation date")
        return None

    try:
        reader = pypdf.PdfReader(str(filename))
        if reader.metadata is None:
            logger.info(f"No metadata found in PDF {filename}")
            return None
        creation_date = reader.metadata.creation_date
        if creation_date is None:
            logger.info(f"No creation date found in PDF metadata for {filename}")
            return None
        if isinstance(creation_date, datetime.datetime):
            if creation_date.tzinfo is None:
                creation_date = creation_date.replace(tzinfo=datetime.UTC)
            return creation_date
        logger.info(
            f"Unexpected type for creation date in PDF {filename}: {type(creation_date)}"
        )
        return None
    except Exception as e:  # noqa: BLE001
        logger.info(f"Could not read PDF creation date for {filename}: {e}")
        return None


def get_timetouse(
    time_option: Literal["now", "earliest", "latest"], filename: Path
) -> datetime.datetime:
    ctime = datetime.datetime.fromtimestamp(filename.stat().st_ctime, tz=datetime.UTC)
    mtime = datetime.datetime.fromtimestamp(filename.stat().st_mtime, tz=datetime.UTC)

    if time_option == "now":
        timetouse = datetime.datetime.now(tz=datetime.UTC)
    elif time_option == "earliest":
        timetouse = min(ctime, mtime)
    else:
        timetouse = max(ctime, mtime)

    return timetouse


def validate_move(force: bool, original_filename: Path, filename: Path) -> None:
    if filename.exists() and not force:
        raise FatalError(
            f"Want to move {original_filename} to "
            + f"{filename}, but it already exists."
        )


def rlinput(prompt: str, prefill: str = "") -> str:
    if os.name == "nt":
        return input(prompt)
    import readline  # noqa: PLC0415

    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def shiftfile(undo_log_file: Path | None, source: Path, target: Path) -> None:
    logger = logging.getLogger("normfn")

    source = source.resolve()
    target = target.resolve()

    dt_now = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%dT%H-%M-%S")

    try:
        shutil.move(source, target)
    except PermissionError as permission_error:
        filename: str = permission_error.filename  # pyright: ignore[reportAny]
        if filename == source:
            msg = f"Permission denied on source: {filename}"
            raise FatalError(msg) from permission_error

        if filename == target:
            msg = f"Permission denied on target: {filename}"
            raise FatalError(msg) from permission_error

        raise

    if undo_log_file:
        check_undo_log_file_header(undo_log_file)
        with undo_log_file.open("a", encoding="utf-8") as log_file:
            _ = log_file.write(f"# {dt_now}: moving {source} to {target}\n")
            _ = log_file.write(
                f"mv {shlex.quote(str(target))} {shlex.quote(str(source))}\n"
            )
    logger.info(f"{source} moved to {target}")


def check_undo_log_file_header(undo_log_file: Path) -> None:
    if not undo_log_file.exists():
        undo_log_file.parent.mkdir(parents=True, exist_ok=True)
        with undo_log_file.open("w") as log_file:
            wrapper = textwrap.TextWrapper(initial_indent="# ", subsequent_indent="# ")
            _ = log_file.write("#!/bin/sh\n")
            _ = log_file.write(
                wrapper.fill(
                    "File generated by normfn "
                    + "(see http://www.github.com/andrewferrier/normfn). This file is "
                    + "utf-8 encoded)"
                )
                + "\n"
            )
            _ = log_file.write("#\n")
            _ = log_file.write(
                wrapper.fill(
                    "This file contains shell commands which can be "
                    + "run to invert (undo) the effects of "
                    + "running normfn. They must be run in *reverse order*. "
                    + f"You can achieve this by running `tac {undo_log_file}"
                    + " | sh`. If you wish, you can edit "
                    + "the file first to control which actions are undone."
                )
                + "\n"
            )
            _ = log_file.write("#\n")
            _ = log_file.write(
                wrapper.fill(
                    "(Specific note for MacOS: tac may not be installed. "
                    + "You can install gtac, the "
                    + "equivalent command, using `brew install coreutils`. "
                    + "You will need Homebrew - "
                    + "http://brew.sh/ - installed)"
                )
                + "\n"
            )
            _ = log_file.write("\n")


def ask_yes_no(prompt: str) -> bytes:
    while True:
        print(prompt, end="", flush=True)  # noqa: T201
        try:
            key = readchar().lower()
        except KeyboardInterrupt as ki:
            raise _QuitSignal from ki
        print(str(key, "utf-8"))  # noqa: T201
        if key in [b"y", b"n", b"e"]:
            return key
        if key == b"q":
            raise _QuitSignal


def readchar() -> bytes:
    if os.name == "nt":
        import msvcrt  # noqa: PLC0415

        return msvcrt.getch()

    import termios  # noqa: PLC0415
    import tty  # noqa: PLC0415

    try:
        old_settings = termios.tcgetattr(sys.stdin)
        _ = tty.setcbreak(sys.stdin.fileno())
        try:
            return os.read(sys.stdin.fileno(), 1)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    except termios.error:
        return os.read(sys.stdin.fileno(), 1)


def insensitiveize(string: str) -> str:
    return "".join(("[" + char.lower() + char.upper() + "]") for char in string)


def setup_logging() -> tuple[logging.Logger, logging.StreamHandler[TextIOBase]]:
    logger = logging.getLogger("normfn")
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    syserrhandler: logging.StreamHandler[TextIOBase] = logging.StreamHandler(
        stream=cast("TextIOBase", sys.stderr)
    )
    syserrhandler.setLevel(logging.WARNING)
    syserrformatter = logging.Formatter("%(levelname)s: %(message)s")
    syserrhandler.setFormatter(syserrformatter)
    logger.addHandler(syserrhandler)

    return logger, syserrhandler
