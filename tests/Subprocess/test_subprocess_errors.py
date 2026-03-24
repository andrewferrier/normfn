from tests.base_test_classes import NormalizeFilenameTestCase


class TestSubprocessErrors(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_no_files(self) -> None:
        (rc, _, error, _) = self.invoke_as_subprocess([], expect_output=True)
        self.assertEqual(2, rc)
        self.assertEqual(0, self.directory_file_count(self.working_dir))
        self.assertRegex(error, ".*You.*must.*specify.*some.*")
        self.assertNotIn("Traceback", error)
