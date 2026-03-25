from tests.base_test_classes import NormfnTestCase


class TestDirectArguments(NormfnTestCase):
    def test_targetfile_exists_with_force(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.write_file(filename, "original")
        filename2 = self.working_dir / (self.get_date_prefix() + "blah.txt")
        self.write_file(filename2, "new")
        self.invoke_directly([filename], extra_params=["--force"])
        assert not filename.exists()
        assert filename2.exists()
        assert self.read_file(filename2) == "original"
        assert self.directory_file_count(self.working_dir) == 1
