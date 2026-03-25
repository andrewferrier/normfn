import re
from pathlib import Path

from tests.base_test_classes import NormfnTestCase


class TestSubprocessArguments(NormfnTestCase):
    def test_no_basicdateprefix(self) -> None:
        (rc, _, error, _) = self.invoke_as_subprocess(
            [], extra_params=["--help"], expect_output=True
        )
        assert rc == 0
        assert self.directory_file_count(self.working_dir) == 0
        assert error == ""

    def test_verbose(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--verbose"]
        )
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert re.search("moved to", error)

    def test_verbose_impliedby_dryrun(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--dry-run"]
        )
        assert rc == 0
        assert filename.exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert re.search("(?i)not moving.*dry run", error)

    def test_recursive_current_directory(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / "foobar.txt"
        self.touch(filename)
        (rc, _, error, _) = self.invoke_as_subprocess(
            [Path(".")], extra_params=["--recursive"], cwd=sub_working_dir
        )
        assert rc == 0
        assert error == ""
        newsub_working_dir = self.working_dir / (
            self.get_date_prefix() + "subWorkingDir"
        )

        assert not filename.exists()
        assert not sub_working_dir.exists()
        assert (newsub_working_dir / (self.get_date_prefix() + "foobar.txt")).exists()
        assert self.directory_file_count(newsub_working_dir) == 1

    def test_recursive_current_directory_interactive(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / "foobar.txt"
        self.touch(filename)
        (rc, _, error, _) = self.invoke_as_subprocess(
            [Path(".")],
            feed_input=b"ny",
            extra_params=["--interactive", "--recursive"],
            cwd=sub_working_dir,
            expect_output=True,
        )
        assert rc == 0
        assert error == ""
        assert not filename.exists()
        assert sub_working_dir.exists()
        assert (sub_working_dir / (self.get_date_prefix() + "foobar.txt")).exists()
        assert self.directory_file_count(sub_working_dir) == 1

    def test_recursive_current_directory_interactive_with_dotfile(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / ".bar.txt"
        filename2 = sub_working_dir / "foo.txt"
        self.touch(filename)
        self.touch(filename2)
        (rc, _, error, _) = self.invoke_as_subprocess(
            [Path(".")],
            feed_input=b"ny",
            extra_params=["--interactive", "--recursive"],
            cwd=sub_working_dir,
            expect_output=True,
        )
        assert rc == 0
        assert error == ""
        assert filename.exists()
        assert sub_working_dir.exists()
        assert not filename2.exists()
        assert (sub_working_dir / (self.get_date_prefix() + "foo.txt")).exists()
        assert self.directory_file_count(sub_working_dir) == 2

    def test_loads_of_files(self) -> None:
        TOTAL_FILES = 100  # noqa: N806

        filenames = [("filename" + str(i) + ".txt") for i in range(TOTAL_FILES)]
        for filename in filenames:
            self.touch(self.working_dir / filename)
        assert self.directory_file_count(self.working_dir) == TOTAL_FILES
        (rc, _, error, _) = self.invoke_as_subprocess(
            [Path(f) for f in filenames], extra_params=["-vv"]
        )
        assert rc == 0
        assert not re.search("exception", error)
        assert self.directory_file_count(self.working_dir) == TOTAL_FILES
        for filename in filenames:
            assert not (self.working_dir / filename).exists()
            assert (self.working_dir / (self.get_date_prefix() + filename)).exists()
