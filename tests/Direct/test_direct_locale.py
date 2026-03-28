import locale

import pytest

from normfn.dates import _ENGLISH_MONTH_ABBRS, _ENGLISH_MONTH_NAMES
from tests.base_test_classes import NormfnTestCase


def _locale_available(loc: str) -> bool:
    saved = locale.setlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, loc)
    except locale.Error:
        return False
    else:
        return True
    finally:
        locale.setlocale(locale.LC_TIME, saved)


def _require_locale(loc: str) -> None:
    """Skip the test if the required locale is not available."""
    if not _locale_available(loc):
        pytest.skip(
            f"Required locale {loc!r} is not installed on this system.\n"
            f"To install: sudo locale-gen {loc}\n"
        )


class TestEnglishMonthConstants(NormfnTestCase):
    """Verify that English month name constants are captured at import time."""

    def test_english_month_names_captured(self) -> None:
        assert len(_ENGLISH_MONTH_NAMES) == 13  # index 0 is empty string
        assert _ENGLISH_MONTH_NAMES[1].lower() == "january"
        assert _ENGLISH_MONTH_NAMES[12].lower() == "december"

    def test_english_month_abbrs_captured(self) -> None:
        assert len(_ENGLISH_MONTH_ABBRS) == 13
        assert _ENGLISH_MONTH_ABBRS[1].lower() == "jan"
        assert _ENGLISH_MONTH_ABBRS[12].lower() == "dec"


class TestLocaleMonthNames(NormfnTestCase):
    def test_english_month_names_always_recognised(self) -> None:
        filename = self.working_dir / "Report 25 January 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-01-25-Report.txt").exists()

    def test_english_abbr_month_names_always_recognised(self) -> None:
        filename = self.working_dir / "Report 25 Jan 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-01-25-Report.txt").exists()

    def test_german_month_names_recognised(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _require_locale("de_DE.UTF-8")
        monkeypatch.setenv("LC_TIME", "de_DE.UTF-8")
        filename = self.working_dir / "Bericht 25 Januar 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-01-25-Bericht.txt").exists()

    def test_german_abbr_month_names_recognised(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _require_locale("de_DE.UTF-8")
        monkeypatch.setenv("LC_TIME", "de_DE.UTF-8")
        filename = self.working_dir / "Bericht 03 Mär 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-03-03-Bericht.txt").exists()

    def test_french_month_names_recognised(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _require_locale("fr_FR.UTF-8")
        monkeypatch.setenv("LC_TIME", "fr_FR.UTF-8")
        filename = self.working_dir / "Rapport 25 janvier 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-01-25-Rapport.txt").exists()

    def test_french_abbr_month_names_recognised(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _require_locale("fr_FR.UTF-8")
        monkeypatch.setenv("LC_TIME", "fr_FR.UTF-8")
        filename = self.working_dir / "Rapport 14 juil. 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-07-14-Rapport.txt").exists()

    def test_english_still_works_with_non_english_locale(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _require_locale("de_DE.UTF-8")
        monkeypatch.setenv("LC_TIME", "de_DE.UTF-8")
        filename = self.working_dir / "Report 25 January 2015.txt"
        self.touch(filename)
        self.invoke_directly([filename])
        assert (self.working_dir / "2015-01-25-Report.txt").exists()
