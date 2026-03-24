import os
import re

from tests.base_test_classes import NormalizeFilenameTestCase


class TestDirectErrors(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_file_not_exist(self) -> None:
        filename = self.working_dir / "blah.txt"
        with self.assertRaisesRegex(Exception, "does.*.not.*exist"):
            self.invoke_directly([filename])
        self.assertFalse(filename.exists())
        self.assertFalse(
            (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        )
        self.assertEqual(0, self.directory_file_count(self.working_dir))

    def test_targetfile_exists(self) -> None:
        if os.name == "nt":
            self.skipTest(
                "FIXME: This test passes on Windows by "
                "inspection, but the automation doesn't work."
            )
        else:
            filename = self.working_dir / "blah.txt"
            self.write_file(filename, "original")
            filename2 = self.working_dir / (self.get_date_prefix() + "blah.txt")
            self.write_file(filename2, "new")
            with self.assertRaisesRegex(
                Exception, re.escape(str(filename2)) + ".*exists"
            ):
                self.invoke_directly([filename])
            self.assertTrue(filename.exists())
            self.assertTrue(filename2.exists())
            self.assertEqual(self.read_file(filename), "original")
            self.assertEqual(self.read_file(filename2), "new")
            self.assertEqual(2, self.directory_file_count(self.working_dir))

    def test_rename_nopermissions(self) -> None:
        if os.name == "nt":
            self.skipTest("Not valid on Windows.")
        elif self.is_root():
            self.skipTest("Am root.")
        else:
            subdirectory = self.working_dir / "subdirectory"
            filename = subdirectory / "blah.txt"
            self.touch(filename)
            self.remove_dir_write_permissions(subdirectory)
            with self.assertRaisesRegex(Exception, "(?i).*permission denied.*"):
                self.invoke_directly([filename])
            self.assertTrue(filename.exists())
            self.assertEqual(1, self.directory_file_count(subdirectory))
