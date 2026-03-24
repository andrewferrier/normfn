import datetime
import io
import logging
import os
import os.path
import shutil
import sys
import tempfile
import types
import unittest
from contextlib import contextmanager
from pathlib import Path
from stat import S_IRUSR, S_IWUSR, S_IXUSR
from subprocess import PIPE, Popen, call
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from io import TextIOBase

import pexpect

from normfn.core import main

COMMAND = [sys.executable, "-m", "normfn"]


class NormalizeFilenameTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.working_dir: Path = Path(tempfile.mkdtemp())

    def get_date_prefix(self, postfix_dash: bool = True) -> str:  # noqa: FBT002
        str_return = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d")
        if postfix_dash is True:
            str_return = str_return + "-"

        return str_return

    def directory_file_count(self, directory: Path) -> int:
        return len(
            [item for item in directory.iterdir() if (directory / item).is_file()]
        )

    def directory_dir_count(self, directory: Path) -> int:
        return len(
            [item for item in directory.iterdir() if (directory / item).is_dir()]
        )

    def invoke_directly(
        self, input_files: list[Path], extra_params: list[str] | None = None
    ) -> str:
        if extra_params is None:
            extra_params = []

        options: list[str] = ["normfn"]

        options.extend([str(p) for p in input_files])
        options.extend(extra_params)
        options.extend(["--no-undo-log-file"])

        stream = io.StringIO()
        handler: logging.StreamHandler[TextIOBase] = logging.StreamHandler(
            stream=cast("TextIOBase", stream)
        )
        log = logging.getLogger("normfn")
        log.propagate = False
        log.setLevel(logging.DEBUG)
        log.addHandler(handler)

        try:
            main(options, handler)
        finally:
            log.removeHandler(handler)
            handler.close()

        return stream.getvalue()

    def invoke_as_subprocess(  # noqa: PLR0913
        self,
        input_files: list[Path],
        extra_params: list[str] | None = None,
        feed_input: bytes | None = None,
        cwd: Path | None = None,
        expect_output: bool = False,  # noqa: FBT002
        use_undo_file: bool = False,  # noqa: FBT002
    ) -> tuple[int, str, str, list[str] | None]:
        if extra_params is None:
            extra_params = []

        if cwd is None:
            cwd = Path(self.working_dir)

        with tempfile.NamedTemporaryFile(delete=False) as undo_log_file:
            undo_log_file.close()

            options: list[str] = list(COMMAND)

            options.extend([str(p) for p in input_files])
            options.extend(extra_params)
            options.extend(["--undo-log-file=" + undo_log_file.name])

            if feed_input:
                p = Popen(options, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)  # noqa: S603
            else:
                p = Popen(options, stdin=None, stdout=PIPE, stderr=PIPE, cwd=cwd)  # noqa: S603

            output_bytes, error_bytes = p.communicate(feed_input)
            p.wait()

            output = output_bytes.decode("utf-8")
            error = error_bytes.decode("utf-8")

            if expect_output:
                self.assertNotEqual("", output)
            else:
                self.assertEqual("", output)

            with open(undo_log_file.name) as undo_log_file_read:  # noqa: PTH123
                undo_log_file_contents = undo_log_file_read.readlines()

            os.unlink(undo_log_file.name)  # noqa: PTH108

        if use_undo_file:
            return (p.returncode, output, error, undo_log_file_contents)

        return (p.returncode, output, error, None)

    def execute_undo_commands(self, commands: list[str]) -> int:
        max_return_code: int = 0
        reversed_commands = commands
        reversed_commands.reverse()
        for command in reversed_commands:
            command_to_call = command.rstrip("\n\r")
            max_return_code = max(max_return_code, call(command_to_call, shell=True))  # noqa: S602

        return max_return_code

    @contextmanager
    def invoke_as_pexpect(
        self,
        input_files: list[Path],
        extra_params: list[str] | None = None,
        expected_exit_status: int | None = None,
        expected_output_regex: str | None = None,
    ) -> types.GeneratorType:
        if extra_params is None:
            extra_params = []

        options: list[str] = list(COMMAND)
        options.extend(str(p) for p in input_files)
        options.extend(extra_params)
        options.extend(["--no-undo-log-file"])

        command = " ".join(options)

        stream = io.BytesIO()

        child = pexpect.spawn(command)
        child.logfile_read = stream

        yield child

        child.expect(pexpect.EOF)
        child.close()

        if expected_exit_status is not None:
            self.assertEqual(expected_exit_status, child.exitstatus)

        if expected_output_regex is not None:
            self.assertRegex(
                str(child.logfile_read.getvalue(), "utf-8"), expected_output_regex
            )

    def touch(self, fname: Path) -> None:
        fname.parent.mkdir(parents=True, exist_ok=True)
        fname.open("w").close()

    def remove_dir_write_permissions(self, fname: Path) -> None:
        fname.chmod(S_IRUSR | S_IXUSR)

    def write_file(self, fname: Path, contents: str) -> None:
        fname.parent.mkdir(parents=True, exist_ok=True)
        with fname.open("w") as filename:
            filename.write(contents)

    def read_file(self, fname: Path) -> str:
        with fname.open() as filename:
            return filename.read()

    def assert_path_doesnt_exist(self, path: Path) -> None:
        self.assertFalse(path.exists())

    def assert_path_exists(self, path: Path) -> None:
        self.assertTrue(path.exists())

    def is_root(self) -> bool:
        return os.geteuid() == 0

    def tear_down(self) -> None:
        # Give everything write permissions before rmtree'ing.
        for root, dirs, files in os.walk(self.working_dir):
            dirs_and_files = dirs + files
            for dir_and_file in dirs_and_files:
                (Path(root) / dir_and_file).chmod(S_IRUSR | S_IWUSR | S_IXUSR)

        shutil.rmtree(self.working_dir)
