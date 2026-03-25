import re

from tests.base_test_classes import NormfnTestCase


class TestSubprocessErrors(NormfnTestCase):
    def test_no_files(self) -> None:
        (rc, _, error, _) = self.invoke_as_subprocess([], expect_output=True)
        assert rc == 2
        assert self.directory_file_count(self.working_dir) == 0
        assert re.search(".*You.*must.*specify.*some.*", error)
        assert "Traceback" not in error
