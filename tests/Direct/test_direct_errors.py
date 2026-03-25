import os
import re

import pytest

from tests.base_test_classes import NormfnTestCase


class TestDirectErrors(NormfnTestCase):
    def test_file_not_exist(self) -> None:
        filename = self.working_dir / "blah.txt"
        with pytest.raises(Exception, match=r"does.*.not.*exist"):
            self.invoke_directly([filename])
        assert not filename.exists()
        assert not (self.working_dir / (self.get_date_prefix() + "blah.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 0

    def test_targetfile_exists(self) -> None:
        if os.name == "nt":
            pytest.skip(
                "FIXME: This test passes on Windows by "
                "inspection, but the automation doesn't work."
            )
        filename = self.working_dir / "blah.txt"
        self.write_file(filename, "original")
        filename2 = self.working_dir / (self.get_date_prefix() + "blah.txt")
        self.write_file(filename2, "new")
        with pytest.raises(Exception, match=re.escape(str(filename2)) + ".*exists"):
            self.invoke_directly([filename])
        assert filename.exists()
        assert filename2.exists()
        assert self.read_file(filename) == "original"
        assert self.read_file(filename2) == "new"
        assert self.directory_file_count(self.working_dir) == 2

    def test_rename_nopermissions(self) -> None:
        if os.name == "nt":
            pytest.skip("Not valid on Windows.")
        elif self.is_root():
            pytest.skip("Am root.")
        subdirectory = self.working_dir / "subdirectory"
        filename = subdirectory / "blah.txt"
        self.touch(filename)
        self.remove_dir_write_permissions(subdirectory)
        with pytest.raises(Exception, match=r"(?i).*permission denied.*"):
            self.invoke_directly([filename])
        assert filename.exists()
        assert self.directory_file_count(subdirectory) == 1
