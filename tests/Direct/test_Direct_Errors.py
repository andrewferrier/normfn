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
