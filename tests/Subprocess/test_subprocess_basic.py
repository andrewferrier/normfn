import re
from pathlib import Path

from tests.base_test_classes import NormalizeFilenameTestCase


class TestSubprocessBasic(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_basicdateprefix(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdateprefix_cwd(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [Path("blah.txt")], cwd=self.working_dir
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_nodatemoveneeded(self) -> None:
        filename = self.working_dir / "2015-01-01-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(filename.exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_nodatemoveneeded2(self) -> None:
        filename = self.working_dir / "2015-01-01T12-00-00-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(filename.exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_nodatemoveneeded_partial(self) -> None:
        filename = self.working_dir / "2015-01-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertTrue(filename.exists())
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdatemove(self) -> None:
        filename = self.working_dir / "blah-2015-01-01.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-01-blah.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdatemove_partial(self) -> None:
        filename = self.working_dir / "blah-2015-01.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-blah.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_datemove_partial(self) -> None:
        filename = self.working_dir / "blah-2015-01-bling.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-blah-bling.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdatemove_underscore(self) -> None:
        filename = self.working_dir / "blah_2015_01_01.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-01-blah.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdatemove2(self) -> None:
        filename = self.working_dir / "blah-2015-01-01-bling.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-01-blah-bling.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdatemove2_underscore(self) -> None:
        filename = self.working_dir / "blah_2015_01_01_bling.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-01-blah_bling.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_basicdateprefix_interactive_yes(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename],
            feed_input=b"y",
            extra_params=["--interactive"],
            expect_output=True,
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertRegex(output, "Move " + re.escape(str(filename)) + ".*")
        self.assertEqual("", error)

    def test_basicdateprefix_interactive_no(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename],
            feed_input=b"n",
            extra_params=["--interactive"],
            expect_output=True,
        )
        self.assertEqual(0, rc)
        self.assertTrue(filename.exists())
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertRegex(output, "Move " + re.escape(str(filename)) + ".*")
        self.assertEqual("", error)

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
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assertTrue(filename2.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        )
        self.assertEqual(2, self.directory_file_count(self.working_dir))
        self.assertRegex(
            output,
            "(?is)Move "
            + re.escape(str(filename))
            + ".*Move "
            + re.escape(str(filename2))
            + ".*",
        )
        self.assertEqual("", error)

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
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assertTrue(filename2.exists())
        self.assertTrue(filename3.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        )
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah3.txt")).exists()
        )
        self.assertEqual(3, self.directory_file_count(self.working_dir))
        self.assertRegex(
            output,
            "(?is)Move "
            + re.escape(str(filename))
            + ".*Move "
            + re.escape(str(filename2))
            + ".*",
        )
        self.assertEqual("", error)

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

        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "bling.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))

    def test_logfile(self) -> None:
        filename = self.working_dir / "blah.txt"
        filename2 = self.working_dir / "blah2.txt"
        self.touch(filename)
        self.touch(filename2)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [filename, filename2], use_undo_file=True
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assertFalse(filename2.exists())
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertTrue(
            (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        )
        self.assertEqual(2, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)
        self.assertEqual(0, self.execute_undo_commands(undo_log_lines))
        self.assertTrue(filename.exists())
        self.assertTrue(filename2.exists())
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah2.txt")).exists()
        )
        self.assertEqual(2, self.directory_file_count(self.working_dir))

    def test_logfile_with_spaces(self) -> None:
        filename = self.working_dir / "sub dir" / "foo bar.txt"
        self.touch(filename)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [filename], use_undo_file=True
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(
            self.working_dir / "sub dir" / (self.get_date_prefix() + "foo bar.txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir / "sub dir"))
        self.assertEqual("", error)
        self.assertEqual(0, self.execute_undo_commands(undo_log_lines))
        self.assertTrue(filename.exists())
        self.assert_path_doesnt_exist(
            self.working_dir / "sub dir" / (self.get_date_prefix() + "foo bar.txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir / "sub dir"))

    def test_logfile_with_single_quotes(self) -> None:
        filename = self.working_dir / "sub'dir" / "foo'bar.txt"
        self.touch(filename)
        (rc, _, error, undo_log_lines) = self.invoke_as_subprocess(
            [filename], use_undo_file=True
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(
            self.working_dir / "sub'dir" / (self.get_date_prefix() + "foo'bar.txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir / "sub'dir"))
        self.assertEqual("", error)
        self.assertEqual(0, self.execute_undo_commands(undo_log_lines))
        self.assertTrue(filename.exists())
        self.assert_path_doesnt_exist(
            self.working_dir / "sub'dir" / (self.get_date_prefix() + "foo'bar.txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir / "sub'dir"))

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
        self.assertEqual(0, rc)
        self.assertEqual("", error)
        newsub_working_dir = self.working_dir / (
            self.get_date_prefix() + "subWorkingDir"
        )
        self.assert_path_doesnt_exist(filename)
        self.assert_path_doesnt_exist(filename2)
        self.assert_path_doesnt_exist(filename3)
        self.assert_path_exists(newsub_working_dir / "2015-01-01-blah_bling.txt")
        self.assert_path_exists(newsub_working_dir / "2015-03-04-xyz.txt")
        self.assert_path_exists(
            newsub_working_dir
            / (self.get_date_prefix() + "subWorkingDir2")
            / "2015-03-04-abc.txt"
        )
        self.assertEqual(2, self.directory_file_count(newsub_working_dir))
        self.assertEqual(
            1,
            self.directory_file_count(
                newsub_working_dir / (self.get_date_prefix() + "subWorkingDir2")
            ),
        )
        self.assertEqual(0, self.execute_undo_commands(undo_log_lines))
        self.assert_path_doesnt_exist(newsub_working_dir)
        self.assert_path_exists(filename)
        self.assert_path_exists(filename2)
        self.assert_path_exists(filename3)
        self.assertEqual(2, self.directory_file_count(sub_working_dir))
        self.assertEqual(
            1, self.directory_file_count(sub_working_dir / "subWorkingDir2")
        )

    def test_discardprevioussuffix(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--discard-existing-name"]
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(
            self.working_dir / (self.get_date_prefix(postfix_dash=False) + ".txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)

    def test_discardprevioussuffix_existingdate(self) -> None:
        filename = self.working_dir / "2015-01-01-blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--discard-existing-name"]
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(self.working_dir / "2015-01-01.txt")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertEqual("", error)
