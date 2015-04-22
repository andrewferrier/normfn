import os
import tempfile

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestDirectArguments(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestDirectArguments, self).setUp()

    def test_backup_directory(self):
        with tempfile.TemporaryDirectory(dir='/tmp') as backupDir:
            filename = os.path.join(self.workingDir, 'blah.txt')
            self.touch(filename)
            error = self.invokeDirectly([filename], extraParams=['--backup-directory=' + backupDir])
            self.assertFalse(os.path.exists(filename))
            self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
            self.assertEqual(1, self.directoryFileCount(self.workingDir))
            self.assertTrue(os.path.exists(os.path.join(backupDir, 'blah.txt')))
            self.assertFalse(os.path.exists(os.path.join(backupDir, self.getDatePrefix() + 'blah.txt')))
            self.assertEqual(1, self.directoryFileCount(backupDir))
            self.assertEqual('', error)

    def test_backup_directory_doesnt_exist(self):
        with tempfile.TemporaryDirectory(dir='/tmp') as backupDir:
            pass

        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        with self.assertRaisesRegex(Exception, "does.*.not.*exist"):
            self.invokeDirectly([filename], extraParams=['--backup-directory=' + backupDir])
        self.assertTrue(os.path.exists(filename))
        self.assertFalse(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertFalse(os.path.exists(os.path.join(backupDir, 'blah.txt')))
        self.assertFalse(os.path.exists(os.path.join(backupDir, self.getDatePrefix() + 'blah.txt')))

    def test_addtime(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        error = self.invokeDirectly([filename], extraParams=['--add-time'])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDateAndTimePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', error)
