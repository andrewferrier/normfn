import os

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestDirectErrors(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestDirectErrors, self).setUp()

    def test_file_not_exist(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        with self.assertRaisesRegex(Exception, "does.*.not.*exist"):
            self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(0, self.directoryFileCount(self.workingDir))

    def test_targetfile_exists(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.writeFile(filename, "original")
        filename2 = os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')
        self.writeFile(filename2, "new")
        with self.assertRaisesRegex(Exception, filename2 + ".*exists"):
            self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertTrue(os.path.exists(filename2))
        self.assertEqual(self.readFile(filename), "original")
        self.assertEqual(self.readFile(filename2), "new")
        self.assertEqual(2, self.directoryFileCount(self.workingDir))

    def test_rename_nopermissions(self):
        if not self.isRoot():
            subdirectory = os.path.join(self.workingDir, 'subdirectory')
            filename = os.path.join(subdirectory, 'blah.txt')
            self.touch(filename)
            self.remove_dir_write_permissions(subdirectory)
            with self.assertRaisesRegex(Exception, "(?i).*permission denied.*"):
                self.invokeDirectly([filename])
            self.assertTrue(os.path.exists(filename))
            self.assertEqual(1, self.directoryFileCount(subdirectory))
        else:
            self.skipTest("Am root.")
