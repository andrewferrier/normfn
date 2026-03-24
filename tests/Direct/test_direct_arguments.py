from tests.base_test_classes import NormalizeFilenameTestCase


class TestDirectArguments(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_targetfile_exists_with_force(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.write_file(filename, "original")
        filename2 = self.working_dir / (self.get_date_prefix() + "blah.txt")
        self.write_file(filename2, "new")
        self.invoke_directly([filename], extra_params=["--force"])
        self.assertFalse(filename.exists())
        self.assertTrue(filename2.exists())
        self.assertEqual(self.read_file(filename2), "original")
        self.assertEqual(1, self.directory_file_count(self.working_dir))
