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
