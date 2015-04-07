import os

from freezegun import freeze_time
from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestBasic, self).setUp()

    def test_no_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=['--no-prefix-date'])
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)
