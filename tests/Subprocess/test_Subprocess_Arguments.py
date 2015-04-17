from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestSubprocessArguments(NormalizeFilenameTestCase):
    def setUp(self):
        super(TestSubprocessArguments, self).setUp()

    def test_no_basicdateprefix(self):
        (rc, output, error) = self.invokeAsSubprocess([], extraParams=['--help'], expectOutput=True)
        self.assertEqual(0, rc)
        self.assertEqual(0, self.directoryCount(self.workingDir))
        self.assertEqual('', error)
