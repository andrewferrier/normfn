import os

from freezegun import freeze_time
from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestErrors(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestErrors, self).setUp()

    def test_file_not_exist(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        with self.assertRaisesRegex(Exception, "does.*.not.*exist"):
            error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(0, self.directoryCount(self.workingDir))