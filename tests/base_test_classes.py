import datetime
import io
import logging
import os
import re
import sys
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from stat import S_IRUSR, S_IXUSR
from subprocess import PIPE, Popen, call
from typing import TYPE_CHECKING, cast

import pexpect
import pytest

if TYPE_CHECKING:
    from io import TextIOBase

from normfn.core import main

COMMAND = [sys.executable, "-m", "normfn"]


class NormfnTestCase:
    working_dir: Path
    config_file: Path

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        self.working_dir = tmp_path
        normfn_config_dir = tmp_path / "xdg_config" / "normfn"
        normfn_config_dir.mkdir(parents=True)
        self.config_file = normfn_config_dir / "normfn.toml"
        self.config_file.write_text("")
        monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))

    def get_date_prefix(self, postfix_dash: bool = True) -> str:  # noqa: FBT002
        local_now = datetime.datetime.now(datetime.UTC).astimezone()
        str_return = local_now.strftime("%Y-%m-%d")
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

    def write_config(self, contents: str) -> None:
        self.config_file.write_text(contents)

    def invoke_directly(
        self,
        input_files: list[Path],
        extra_params: list[str] | None = None,
    ) -> str:
        if extra_params is None:
            extra_params = []

        options: list[str] = ["normfn", "--config", str(self.config_file)]
        options.extend([str(p) for p in input_files])
        options.extend(extra_params)

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

        options: list[str] = list(COMMAND)
        options.extend(["--config", str(self.config_file)])
        options.extend([str(p) for p in input_files])
        options.extend(extra_params)

        if use_undo_file:
            with tempfile.NamedTemporaryFile(
                dir=self.working_dir, suffix=".sh", delete=False
            ) as tf:
                undo_log_path = Path(tf.name)
            with self.config_file.open("a") as f:
                f.write(f'undo_log_file = "{undo_log_path}"\n')

        env = {**os.environ}

        if feed_input:
            p = Popen(options, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env)  # noqa: S603
        else:
            p = Popen(options, stdin=None, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env)  # noqa: S603

        output_bytes, error_bytes = p.communicate(feed_input)
        p.wait()

        output = output_bytes.decode("utf-8")
        error = error_bytes.decode("utf-8")

        if expect_output:
            assert output != ""
        else:
            assert output == ""

        if use_undo_file:
            undo_log_file_contents = (
                undo_log_path.read_text().splitlines(keepends=True)
                if undo_log_path.exists()
                else []
            )
            if undo_log_path.exists():
                undo_log_path.unlink()
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
    ) -> Iterator[pexpect.spawn]:
        if extra_params is None:
            extra_params = []

        options: list[str] = list(COMMAND)
        options.extend(["--config", str(self.config_file)])
        options.extend(str(p) for p in input_files)
        options.extend(extra_params)

        env = {**os.environ}
        command = " ".join(options)

        stream = io.BytesIO()

        child = pexpect.spawn(command, env=env)
        child.logfile_read = stream

        yield child

        child.expect(pexpect.EOF)
        child.close()

        if expected_exit_status is not None:
            assert child.exitstatus == expected_exit_status

        if expected_output_regex is not None:
            assert re.search(
                expected_output_regex, str(child.logfile_read.getvalue(), "utf-8")
            )

    def set_local_timezone(
        self,
        tz: str,
        request: pytest.FixtureRequest,
    ) -> None:
        """
        Set the local timezone for a test, restoring it on teardown.

        POSIX TZ convention note: the offset sign is *inverted* vs ISO 8601.
        TZ='UTC-2' means local time = UTC + 2 hours (i.e. UTC+2).
        TZ='UTC+5' means local time = UTC - 5 hours (i.e. UTC-5).
        """
        original_tz = os.environ.get("TZ")
        os.environ["TZ"] = tz
        time.tzset()

        def _restore() -> None:
            if original_tz is None:
                os.environ.pop("TZ", None)
            else:
                os.environ["TZ"] = original_tz
            time.tzset()

        request.addfinalizer(_restore)

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

    def is_root(self) -> bool:
        return os.geteuid() == 0
