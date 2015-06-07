import os
import tempfile

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestDirectArguments(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestDirectArguments, self).setUp()

    def test_targetfile_exists_with_force(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.writeFile(filename, "original")
        filename2 = os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')
        self.writeFile(filename2, "new")
        self.invokeDirectly([filename], extraParams=['--force'])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(filename2))
        self.assertEqual(self.readFile(filename2), "original")
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
