from tests.BaseTestClasses import NormalizeFilenameTestCase


class TestSubprocessErrors(NormalizeFilenameTestCase):
    def setUp(self):
        super().setUp()

    def test_no_files(self):
        (rc, output, error) = self.invokeAsSubprocess([], expectOutput=True)
        self.assertEqual(2, rc)
        self.assertEqual(0, self.directoryFileCount(self.workingDir))
        self.assertRegex(error, ".*You.*must.*specify.*some.*")
