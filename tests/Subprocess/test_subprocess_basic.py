import re
from pathlib import Path

from tests.base_test_classes import NormfnTestCase


class TestSubprocessBasic(NormfnTestCase):
    def test_basicdateprefix(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdateprefix_cwd(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [Path("blah.txt")], cwd=self.working_dir
        )
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_nodatemoveneeded(self) -> None:
        filename = self.working_dir / "2015-01-01-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert filename.exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_nodatemoveneeded2(self) -> None:
        filename = self.working_dir / "2015-01-01T12-00-00-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert filename.exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_nodatemoveneeded_partial(self) -> None:
        filename = self.working_dir / "2015-01-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert filename.exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdatemove(self) -> None:
        filename = self.working_dir / "blah-2015-01-01.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdatemove_partial(self) -> None:
        filename = self.working_dir / "blah-2015-01.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_datemove_partial(self) -> None:
        filename = self.working_dir / "blah-2015-01-bling.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-blah-bling.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdatemove_underscore(self) -> None:
        filename = self.working_dir / "blah_2015_01_01.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdatemove2(self) -> None:
        filename = self.working_dir / "blah-2015-01-01-bling.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01-blah-bling.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdatemove2_underscore(self) -> None:
        filename = self.working_dir / "blah_2015_01_01_bling.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01-blah_bling.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_basicdateprefix_interactive_yes(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename],
            feed_input=b"y",
            extra_params=["--interactive"],
            expect_output=True,
        )
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert re.search("Move " + re.escape(str(filename)) + ".*", output)
        assert error == ""

    def test_basicdateprefix_interactive_no(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename],
            feed_input=b"n",
            extra_params=["--interactive"],
            expect_output=True,
        )
        assert rc == 0
        assert filename.exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert re.search("Move " + re.escape(str(filename)) + ".*", output)
        assert error == ""

    def test_basicdateprefix_interactive_oneyesoneno(self) -> None:
        filename = self.working_dir / "blah.txt"
        filename2 = self.working_dir / "blah2.txt"
        self.touch(filename)
        self.touch(filename2)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename, filename2],
            feed_input=b"yn",
            extra_params=["--interactive"],
            expect_output=True,
        )
        assert rc == 0
        assert not filename.exists()
        assert filename2.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 2
        assert re.search(
            "(?is)Move "
            + re.escape(str(filename))
            + ".*Move "
            + re.escape(str(filename2))
            + ".*",
            output,
        )
        assert error == ""

    def test_basicdateprefix_interactive_oneyesquit(self) -> None:
        filename = self.working_dir / "blah.txt"
        filename2 = self.working_dir / "blah2.txt"
        filename3 = self.working_dir / "blah3.txt"
        self.touch(filename)
        self.touch(filename2)
        self.touch(filename3)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename, filename2, filename3],
            feed_input=b"yqy",
            extra_params=["--interactive"],
            expect_output=True,
        )
        assert rc == 0
        assert not filename.exists()
        assert filename2.exists()
        assert filename3.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah3.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 3
        assert re.search(
            "(?is)Move "
            + re.escape(str(filename))
            + ".*Move "
            + re.escape(str(filename2))
            + ".*",
            output,
        )
        assert error == ""

    def test_basicdateprefix_interactive_edit(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        with self.invoke_as_pexpect(
            [filename],
            extra_params=["--interactive"],
            expected_exit_status=0,
            expected_output_regex="Move " + re.escape(str(filename)) + ".*",
        ) as child:
            child.expect("]? ")
            child.send("e")
            child.expect("filename\\? ")
            for _ in range(19):
                child.sendcontrol("H")
            child.send("bling.txt\n")

        assert not filename.exists()
        assert (self.working_dir / "bling.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_logfile(self) -> None:
        filename = self.working_dir / "blah.txt"
        filename2 = self.working_dir / "blah2.txt"
        self.touch(filename)
        self.touch(filename2)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [filename, filename2], use_undo_file=True
        )
        assert rc == 0
        assert not filename.exists()
        assert not filename2.exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 2
        assert error == ""
        assert undo_log_lines is not None
        assert self.execute_undo_commands(undo_log_lines) == 0
        assert filename.exists()
        assert filename2.exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 2

    def test_logfile_with_spaces(self) -> None:
        filename = self.working_dir / "sub dir" / "foo bar.txt"
        self.touch(filename)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [filename], use_undo_file=True
        )
        assert rc == 0
        assert not filename.exists()
        assert (
            self.working_dir / "sub dir" / (self.get_date_prefix() + "foo bar.txt")
        ).exists()
        assert self.directory_file_count(self.working_dir / "sub dir") == 1
        assert error == ""
        assert undo_log_lines is not None
        assert self.execute_undo_commands(undo_log_lines) == 0
        assert filename.exists()
        assert not (
            self.working_dir / "sub dir" / (self.get_date_prefix() + "foo bar.txt")
        ).exists()
        assert self.directory_file_count(self.working_dir / "sub dir") == 1

    def test_logfile_with_single_quotes(self) -> None:
        filename = self.working_dir / "sub'dir" / "foo'bar.txt"
        self.touch(filename)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [filename], use_undo_file=True
        )
        assert rc == 0
        assert not filename.exists()
        assert (
            self.working_dir / "sub'dir" / (self.get_date_prefix() + "foo'bar.txt")
        ).exists()
        assert self.directory_file_count(self.working_dir / "sub'dir") == 1
        assert error == ""
        assert undo_log_lines is not None
        assert self.execute_undo_commands(undo_log_lines) == 0
        assert filename.exists()
        assert not (
            self.working_dir / "sub'dir" / (self.get_date_prefix() + "foo'bar.txt")
        ).exists()
        assert self.directory_file_count(self.working_dir / "sub'dir") == 1

    def test_directory_withfiles_recursive_logfile(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / "blah_2015_01_01_bling.txt"
        self.touch(filename)
        filename2 = sub_working_dir / "xyz-2015-03-04.txt"
        self.touch(filename2)
        filename3 = sub_working_dir / "subWorkingDir2" / "abc-2015-03-04.txt"
        self.touch(filename3)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [sub_working_dir], extra_params=["--recursive"], use_undo_file=True
        )
        assert rc == 0
        assert error == ""
        newsub_working_dir = self.working_dir / (
            self.get_date_prefix() + "subWorkingDir"
        )
        assert not filename.exists()
        assert not filename2.exists()
        assert not filename3.exists()
        assert (newsub_working_dir / "2015-01-01-blah_bling.txt").exists()
        assert (newsub_working_dir / "2015-03-04-xyz.txt").exists()
        assert (
            newsub_working_dir
            / (self.get_date_prefix() + "subWorkingDir2")
            / "2015-03-04-abc.txt"
        ).exists()
        assert self.directory_file_count(newsub_working_dir) == 2
        assert (
            self.directory_file_count(
                newsub_working_dir / (self.get_date_prefix() + "subWorkingDir2")
            )
            == 1
        )
        assert undo_log_lines is not None
        assert self.execute_undo_commands(undo_log_lines) == 0
        assert not newsub_working_dir.exists()
        assert filename.exists()
        assert filename2.exists()
        assert filename3.exists()
        assert self.directory_file_count(sub_working_dir) == 2
        assert self.directory_file_count(sub_working_dir / "subWorkingDir2") == 1

    def test_discardprevioussuffix(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--discard-existing-name"]
        )
        assert rc == 0
        assert not filename.exists()
        assert (
            self.working_dir / (self.get_date_prefix(postfix_dash=False) + ".txt")
        ).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""

    def test_discardprevioussuffix_existingdate(self) -> None:
        filename = self.working_dir / "2015-01-01-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--discard-existing-name"]
        )
        assert rc == 0
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert output == ""
        assert error == ""
