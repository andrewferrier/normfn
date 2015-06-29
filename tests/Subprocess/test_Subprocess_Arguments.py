import os.path

from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestSubprocessArguments(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestSubprocessArguments, self).setUp()

    def test_no_basicdateprefix(self):
        (rc, output, error) = self.invokeAsSubprocess([], extraParams=['--help'], expectOutput=True)
        self.assertEqual(0, rc)
        self.assertEqual(0, self.directoryFileCount(self.workingDir))
        self.assertEqual('', error)

    def test_verbose(self):
        filename = os.path.join(self.workingDir, 'blah.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess([filename], extraParams=['--verbose'])
        self.assertEqual(0, rc)
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(os.path.exists(os.path.join(self.workingDir, self.getDatePrefix() + 'blah.txt')))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual('', output)
        self.assertRegex(error, 'moved to')

    def test_recursive_current_directory(self):
        subWorkingDir = os.path.join(self.workingDir, 'subWorkingDir')
        filename = os.path.join(subWorkingDir, 'foobar.txt')
        self.touch(filename)
        (rc, output, error) = self.invokeAsSubprocess(['.'], extraParams=['--recursive'], cwd=subWorkingDir)
        self.assertEqual(0, rc)
        self.assertEqual('', error)
        newsubWorkingDir = os.path.join(self.workingDir, self.getDatePrefix() + 'subWorkingDir')
        self.assertPathDoesntExist(filename)
        self.assertPathDoesntExist(subWorkingDir)
        self.assertPathExists(os.path.join(newsubWorkingDir, self.getDatePrefix() + 'foobar.txt'))
        self.assertEqual(1, self.directoryFileCount(newsubWorkingDir))
