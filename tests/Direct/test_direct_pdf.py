import datetime
import io
from pathlib import Path

import pypdf
import pytest

from tests.base_test_classes import NormfnTestCase


def _create_pdf_with_creation_date(
    path: Path, creation_date: datetime.datetime
) -> None:
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    date_str = creation_date.strftime("D:%Y%m%d%H%M%S+00'00'")
    writer.add_metadata({"/CreationDate": date_str})
    buf = io.BytesIO()
    writer.write(buf)
    with path.open("wb") as f:
        f.write(buf.getvalue())


def _create_pdf_without_creation_date(path: Path) -> None:
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    with path.open("wb") as f:
        f.write(buf.getvalue())


def _create_pdf_with_raw_date_string(path: Path, date_str: str) -> None:
    """
    Create a PDF whose /CreationDate metadata is the raw PDF-format string supplied.

    This allows writing PDFs with arbitrary timezones (e.g. '+05'30'') or no
    timezone at all, which the standard helper cannot express.
    """
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_metadata({"/CreationDate": date_str})
    buf = io.BytesIO()
    writer.write(buf)
    with path.open("wb") as f:
        f.write(buf.getvalue())


class TestDirectPDF(NormfnTestCase):
    def test_pdf_creation_date_used(self) -> None:
        filename = self.working_dir / "document.pdf"
        creation_date = datetime.datetime(2015, 2, 3, 10, 11, 12, tzinfo=datetime.UTC)
        _create_pdf_with_creation_date(filename, creation_date)
        error = self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "2015-02-03-document.pdf").exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    def test_pdf_already_has_date_prefix(self) -> None:
        filename = self.working_dir / "2020-01-01-document.pdf"
        creation_date = datetime.datetime(2015, 2, 3, 10, 11, 12, tzinfo=datetime.UTC)
        _create_pdf_with_creation_date(filename, creation_date)
        error = self.invoke_directly([filename])
        assert filename.exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    def test_pdf_without_creation_date_falls_back_to_filesystem(self) -> None:
        filename = self.working_dir / "document.pdf"
        _create_pdf_without_creation_date(filename)
        error = self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / (self.get_date_prefix() + "document.pdf")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    def test_non_pdf_file_unaffected(self) -> None:
        filename = self.working_dir / "document.txt"
        self.touch(filename)
        error = self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / (self.get_date_prefix() + "document.txt")).exists()
        assert self.directory_file_count(self.working_dir) == 1
        assert error == ""

    def test_pdf_utc_date_east_of_utc_crosses_midnight(
        self, request: pytest.FixtureRequest
    ) -> None:
        # TZ=UTC-2 means local is UTC+2.
        # PDF creation date 2015-01-01 23:00:00 UTC = 2015-01-02 01:00:00 locally.
        self.set_local_timezone("UTC-2", request)
        filename = self.working_dir / "document.pdf"
        creation_date = datetime.datetime(2015, 1, 1, 23, 0, 0, tzinfo=datetime.UTC)
        _create_pdf_with_creation_date(filename, creation_date)
        self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-02-document.pdf").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_pdf_utc_date_west_of_utc_crosses_midnight(
        self, request: pytest.FixtureRequest
    ) -> None:
        # TZ=UTC+2 means local is UTC-2.
        # PDF creation date 2015-01-02 01:00:00 UTC = 2015-01-01 23:00:00 locally.
        self.set_local_timezone("UTC+2", request)
        filename = self.working_dir / "document.pdf"
        creation_date = datetime.datetime(2015, 1, 2, 1, 0, 0, tzinfo=datetime.UTC)
        _create_pdf_with_creation_date(filename, creation_date)
        self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-01-document.pdf").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_pdf_non_utc_tz_converted_to_local(
        self, request: pytest.FixtureRequest
    ) -> None:
        # PDF is dated 2015-01-02 23:30:00+05:30 (IST) = 2015-01-02 18:00:00 UTC.
        # TZ=UTC-10 means local is UTC+10: 18:00 UTC = 2015-01-03 04:00:00 locally.
        self.set_local_timezone("UTC-10", request)
        filename = self.working_dir / "document.pdf"
        _create_pdf_with_raw_date_string(filename, "D:20150102233000+05'30'")
        self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-03-document.pdf").exists()
        assert self.directory_file_count(self.working_dir) == 1

    def test_pdf_naive_date_treated_as_local_not_utc(
        self, request: pytest.FixtureRequest
    ) -> None:
        # When a PDF has no timezone in its creation date, the date should be taken
        # at face value (treated as local time, not converted from UTC).
        # A naive date of "2015-01-02 01:00" should always give prefix 2015-01-02,
        # regardless of the local timezone offset.
        #
        # TZ=UTC+5 means local is UTC-5. If the naive date were treated as UTC and
        # then converted to local, 2015-01-02 01:00 UTC → 2015-01-01 20:00 -05:00,
        # which would wrongly give prefix 2015-01-01.
        self.set_local_timezone("UTC+5", request)
        filename = self.working_dir / "document.pdf"
        _create_pdf_with_raw_date_string(filename, "D:20150102010000")
        self.invoke_directly([filename])
        assert not filename.exists()
        assert (self.working_dir / "2015-01-02-document.pdf").exists()
        assert self.directory_file_count(self.working_dir) == 1
