import pytest
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
        self.write_config("max_years_ahead = 50\n")
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2025-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_ok_behind_adjusted(self) -> None:
        filename = self.working_dir / "blah-1970-02-03.txt"
        self.touch(filename)
        self.write_config("max_years_behind = 50\n")
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "1970-02-03-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_ahead_adjusted(self) -> None:
        filename = self.working_dir / "blah-2200-02-03.txt"
        self.touch(filename)
        self.write_config("max_years_ahead = 50\n")
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05-blah-2200-02-03.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:10:10")
    def test_toofar_behind_adjusted(self) -> None:
        filename = self.working_dir / "blah-1930-02-03.txt"
        self.touch(filename)
        self.write_config("max_years_behind = 50\n")
        error = self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05-blah-1930-02-03.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    @freeze_time("2015-04-05 10:11:12")
    def test_addtime(self, request: pytest.FixtureRequest) -> None:
        self.set_local_timezone("UTC", request)
        filename = self.working_dir / "blah.txt"
        self.touch(filename)
        error = self.invoke_directly([filename], extra_params=["--add-time", "--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-04-05T10-11-12-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    def test_now_east_of_utc_crosses_midnight(
        self, request: pytest.FixtureRequest
    ) -> None:
        # TZ=UTC-2 means local is UTC+2.
        # 2015-01-01 23:00:00 UTC = 2015-01-02 01:00:00 locally → date 2015-01-02.
        self.set_local_timezone("UTC-2", request)
        with freeze_time("2015-01-01 23:00:00"):
            filename = self.working_dir / "blah.txt"
            self.touch(filename)
            self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-02-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_now_west_of_utc_crosses_midnight(
        self, request: pytest.FixtureRequest
    ) -> None:
        # TZ=UTC+2 means local is UTC-2.
        # 2015-01-02 01:00:00 UTC = 2015-01-01 23:00:00 locally → date 2015-01-01.
        self.set_local_timezone("UTC+2", request)
        with freeze_time("2015-01-02 01:00:00"):
            filename = self.working_dir / "blah.txt"
            self.touch(filename)
            self.invoke_directly([filename], extra_params=["--now"])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_now_east_of_utc_add_time(self, request: pytest.FixtureRequest) -> None:
        # TZ=UTC-5 means local is UTC+5.
        # 2015-01-01 20:00:00 UTC = 2015-01-02 01:00:00 locally
        # → expected prefix 2015-01-02T01-00-00.
        self.set_local_timezone("UTC-5", request)
        with freeze_time("2015-01-01 20:00:00"):
            filename = self.working_dir / "blah.txt"
            self.touch(filename)
            self.invoke_directly([filename], extra_params=["--now", "--add-time"])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-02T01-00-00-blah.txt").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_year_regex_uses_local_year_at_boundary(
        self, request: pytest.FixtureRequest
    ) -> None:
        # TZ=UTC-2 means local is UTC+2.
        # At 2014-12-31 23:30:00 UTC, local time is 2015-01-01 01:30:00
        # → local year 2015.
        #
        # Year 2019 is 4 years ahead of local year 2015, within max_years_ahead=5
        # (range is year_now + max_years_ahead = 2015+5 = 2020, exclusive → 2019 valid).
        # Using UTC year 2014: 2014+5 = 2019 (exclusive) → 2019 NOT in range.
        #
        # A file named 2019-06-15-blah.txt should be recognised as already having
        # a valid date prefix when local year (2015) is used, and left unchanged.
        self.set_local_timezone("UTC-2", request)
        with freeze_time("2014-12-31 23:30:00"):
            filename = self.working_dir / "2019-06-15-blah.txt"
            self.touch(filename)
            self.invoke_directly([filename], extra_params=["--now"])
        assert filename.exists()
        assert self.directory_file_count(self.working_dir) == 1
