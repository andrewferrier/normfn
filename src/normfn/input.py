import os
import sys

from normfn.exceptions import _QuitSignalError


def ask_yes_no(prompt: str) -> bytes:
    while True:
        print(prompt, end="", flush=True)  # noqa: T201
        try:
            key = readchar().lower()
        except KeyboardInterrupt as ki:
            raise _QuitSignalError from ki
        print(str(key, "utf-8"))  # noqa: T201
        if key in [b"y", b"n", b"e"]:
            return key
        if key == b"q":
            raise _QuitSignalError


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


def rlinput(prompt: str, prefill: str = "") -> str:
    if os.name == "nt":
        return input(prompt)
    import readline  # noqa: PLC0415

    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()
