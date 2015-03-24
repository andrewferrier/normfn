import os

from freezegun import freeze_time
from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestBasic, self).setUp()

    def test_no_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--no-prefix-date'])
        self.assertEqual(0, rc)
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdateprefix(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        print(error)
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual('', output)
        self.assertEqual('', error)

    def test_basicdatemove(self):
        filename = os.path.join(self.workingDir, 'blah-2015-01-01.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual('', output)
        self.assertEqual('', error)
