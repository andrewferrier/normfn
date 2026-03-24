from pathlib import Path

from tests.base_test_classes import NormalizeFilenameTestCase


class TestSubprocessArguments(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_no_basicdateprefix(self) -> None:
        (rc, _, error, _) = self.invoke_as_subprocess(
            [], extra_params=["--help"], expect_output=True
        )
        self.assertEqual(0, rc)
        self.assertEqual(0, self.directory_file_count(self.working_dir))
        self.assertEqual("", error)

    def test_verbose(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--verbose"]
        )
        self.assertEqual(0, rc)
        self.assertFalse(filename.exists())
        self.assert_path_exists(
            self.working_dir / (self.get_date_prefix() + "blah.txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertRegex(error, "moved to")

    def test_verbose_impliedby_dryrun(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        (rc, output, error, _) = self.invoke_as_subprocess(
            [filename], extra_params=["--dry-run"]
        )
        self.assertEqual(0, rc)
        self.assert_path_exists(filename)
        self.assert_path_doesnt_exist(
            self.working_dir / (self.get_date_prefix() + "blah.txt")
        )
        self.assertEqual(1, self.directory_file_count(self.working_dir))
        self.assertEqual("", output)
        self.assertRegex(error, "(?i)not moving.*dry run")

    def test_recursive_current_directory(self) -> None:
        sub_working_dir = self.working_dir / "subWorkingDir"
        filename = sub_working_dir / "foobar.txt"
        self.touch(filename)
        (rc, _, error, _) = self.invoke_as_subprocess(
            [Path(".")], extra_params=["--recursive"], cwd=sub_working_dir
        )
        self.assertEqual(0, rc)
        self.assertEqual("", error)
        newsub_working_dir = self.working_dir / (
            self.get_date_prefix() + "subWorkingDir"
        )

        self.assert_path_doesnt_exist(filename)
        self.assert_path_doesnt_exist(sub_working_dir)
        self.assert_path_exists(
            newsub_working_dir / (self.get_date_prefix() + "foobar.txt")
        )
        self.assertEqual(1, self.directory_file_count(newsub_working_dir))

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
        self.assertEqual(0, rc)
        self.assertEqual("", error)
        self.assert_path_doesnt_exist(filename)
        self.assert_path_exists(sub_working_dir)
        self.assert_path_exists(
            sub_working_dir / (self.get_date_prefix() + "foobar.txt")
        )
        self.assertEqual(1, self.directory_file_count(sub_working_dir))

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
        self.assertEqual(0, rc)
        self.assertEqual("", error)
        self.assert_path_exists(filename)
        self.assert_path_exists(sub_working_dir)
        self.assert_path_doesnt_exist(filename2)
        self.assert_path_exists(sub_working_dir / (self.get_date_prefix() + "foo.txt"))
        self.assertEqual(2, self.directory_file_count(sub_working_dir))

    def test_loads_of_files(self) -> None:
        TOTAL_FILES = 100  # noqa: N806

        filenames = [("filename" + str(i) + ".txt") for i in range(TOTAL_FILES)]
        for filename in filenames:
            self.touch(self.working_dir / filename)
        self.assertEqual(TOTAL_FILES, self.directory_file_count(self.working_dir))
        (rc, _, error, _) = self.invoke_as_subprocess(
            [Path(f) for f in filenames], extra_params=["-vv"]
        )
        self.assertEqual(0, rc)
        self.assertNotRegex(error, "exception")
        self.assertEqual(TOTAL_FILES, self.directory_file_count(self.working_dir))
        for filename in filenames:
            self.assert_path_doesnt_exist(self.working_dir / filename)
            self.assert_path_exists(
                self.working_dir / (self.get_date_prefix() + filename)
            )
