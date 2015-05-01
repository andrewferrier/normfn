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
