import datetime
import io
import os
import unittest

from tests.BaseTestClasses import NormalizeFilenameTestCase


def _create_pdf_with_creation_date(path: str, creation_date: datetime.datetime) -> None:
    try:
        import pypdf  # noqa: PLC0415
    except ImportError:
        raise unittest.SkipTest("pypdf not available")

    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    date_str = creation_date.strftime("D:%Y%m%d%H%M%S+00'00'")
    writer.add_metadata({"/CreationDate": date_str})
    buf = io.BytesIO()
    writer.write(buf)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def _create_pdf_without_creation_date(path: str) -> None:
    try:
        import pypdf  # noqa: PLC0415
    except ImportError:
        raise unittest.SkipTest("pypdf not available")

    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


class TestDirectPDF(NormalizeFilenameTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_pdf_creation_date_used(self) -> None:
        filename = os.path.join(self.workingDir, "document.pdf")
        creation_date = datetime.datetime(2015, 2, 3, 10, 11, 12, tzinfo=datetime.UTC)
        _create_pdf_with_creation_date(filename, creation_date)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(os.path.join(self.workingDir, "2015-02-03-document.pdf"))
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_pdf_already_has_date_prefix(self) -> None:
        filename = os.path.join(self.workingDir, "2020-01-01-document.pdf")
        creation_date = datetime.datetime(2015, 2, 3, 10, 11, 12, tzinfo=datetime.UTC)
        _create_pdf_with_creation_date(filename, creation_date)
        error = self.invokeDirectly([filename])
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_pdf_without_creation_date_falls_back_to_filesystem(self) -> None:
        filename = os.path.join(self.workingDir, "document.pdf")
        _create_pdf_without_creation_date(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "document.pdf")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)

    def test_non_pdf_file_unaffected(self) -> None:
        filename = os.path.join(self.workingDir, "document.txt")
        self.touch(filename)
        error = self.invokeDirectly([filename])
        self.assertFalse(os.path.exists(filename))
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workingDir, self.getDatePrefix() + "document.txt")
            )
        )
        self.assertEqual(1, self.directoryFileCount(self.workingDir))
        self.assertEqual("", error)
