import datetime
import io
from pathlib import Path

import pypdf

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
