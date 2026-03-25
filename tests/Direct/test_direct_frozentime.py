from freezegun import freeze_time

from tests.base_test_classes import NormfnTestCase


class TestDirectFrozenTime(NormfnTestCase):
    @freeze_time("2015-02-03 10:11:12")
    def test_basicdateprefix(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-02-03 10:11:12")
    def test_basicdateprefix_add_time(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([filename], extra_params=["--add-time", "--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-02-03T10-11-12-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-02-03 10:10:10")
    def test_ok_behind(self) -> None:
        filename = self.working_dir / "blah-1990-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "1990-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-02-03 10:10:10")
    def test_ok_ahead(self) -> None:
        filename = self.working_dir / "blah-2019-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "2019-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_behind(self) -> None:
        filename = self.working_dir / "blah-1970-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05-blah-1970-02-03.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_ahead(self) -> None:
        filename = self.working_dir / "blah-2025-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05-blah-2025-02-03.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_ok_ahead_adjusted(self) -> None:
        filename = self.working_dir / "blah-2025-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly(
            [filename], extra_params=["--now", "--max-years-ahead=50"]
        )
        assert not filename.exists()
        assert (self.working_dir / "2025-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_ok_behind_adjusted(self) -> None:
        filename = self.working_dir / "blah-1970-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly(
            [filename], extra_params=["--now", "--max-years-behind=50"]
        )
        assert not filename.exists()
        assert (self.working_dir / "1970-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_ahead_adjusted(self) -> None:
        filename = self.working_dir / "blah-2200-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly(
            [filename], extra_params=["--now", "--max-years-ahead=50"]
        )
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05-blah-2200-02-03.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_behind_adjusted(self) -> None:
        filename = self.working_dir / "blah-1930-02-03.txt"
        self.touch(filename)
        error = self.invoke_directly(
            [filename], extra_params=["--now", "--max-years-behind=50"]
        )
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05-blah-1930-02-03.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:11:12")
    def test_addtime(self) -> None:
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([filename], extra_params=["--add-time", "--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05T10-11-12-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""
