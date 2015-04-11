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

    def test_directory_norecursive(self):
        filename = os.path.join(self.workingDir, 'blah_2015_01_01_bling.txt')
        self.touch(filename)
        filename2 = os.path.join(self.workingDir, '2015-03-04-xyz.txt')
        self.touch(filename2)
        error = self.invokeDirectly([self.workingDir], extraParams=['--no-recursive'])
        self.assertTrue(os.path.exists(filename))
        self.assertTrue(os.path.exists(filename2))
        self.assertEqual(2, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_startswith_period(self):
        filename = os.path.join(self.workingDir, '.blah-2015_01_01.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_startswith_period_all(self):
        filename = os.path.join(self.workingDir, '.blah-2015_01_01.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=['--all'])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-.blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_directory(self):
        filename = os.path.join(self.workingDir, 'blah_2015_01_01_bling.txt')
        self.touch(filename)
        filename2 = os.path.join(self.workingDir, '2015-03-04-xyz.txt')
        self.touch(filename2)
        error = self.invokeDirectly([self.workingDir])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(filename2))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah_bling.txt')))
        self.assertEqual(2, self.directoryCount(self.workingDir))
        self.assertEqual('', error)
