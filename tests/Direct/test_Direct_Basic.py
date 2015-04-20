import datetime
import os

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestDirectBasic(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestDirectBasic, self).setUp()

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

    def test_ridiculousdate1(self):
        filename = os.path.join(self.workingDir, 'blah-2100-01-01.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah-2100-01-01.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_ridiculousdate2(self):
        filename = os.path.join(self.workingDir, 'blah-1899-01-01.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah-1899-01-01.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_invaliddate1(self):
        filename = os.path.join(self.workingDir, 'blah-1990-20-01.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah-1990-20-01.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_invaliddate2(self):
        filename = os.path.join(self.workingDir, 'blah-1990-01-41.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '1990-01-blah-41.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_basic_compressed_datemove(self):
        filename = os.path.join(self.workingDir, 'blah-20150101.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_basic_invalid_compressed_nodatemove(self):
        filename = os.path.join(self.workingDir, 'blah-20153101.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah-20153101.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_basic_compressed_withspace(self):
        filename = os.path.join(self.workingDir, 'blah 20150101.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '2015-01-01-blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_earliest(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        os.utime(filename, (datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                            datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp()))
        error = self.invokeDirectly([filename], extraParams=['--earliest'])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, '1980-01-02-blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_latest(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        os.utime(filename, (datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                            datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp()))
        error = self.invokeDirectly([filename], extraParams=['--latest'])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)

    def test_now(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        os.utime(filename, (datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp(),
                            datetime.datetime(1980, 1, 2, 3, 4, 5).timestamp()))
        error = self.invokeDirectly([filename], extraParams=['--now'])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryCount(self.workingDir))
        self.assertEqual('', error)
