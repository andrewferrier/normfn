import calendar
import datetime
import logging
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from normfn.args import Args
from normfn.files import get_pdf_creation_date, get_timetouse

logger = logging.getLogger(__name__)

# Captured at module import time, before any locale.setlocale() call in main().
# Used to ensure English month names are always recognised even when a
# non-English system locale is active.
_ENGLISH_MONTH_NAMES: Final[list[str]] = list(calendar.month_name)
_ENGLISH_MONTH_ABBRS: Final[list[str]] = list(calendar.month_abbr)


class _InvalidOrdinalError(Exception):
    pass


def insensitiveize(string: str) -> str:
    return "".join(("[" + char.lower() + char.upper() + "]") for char in string)


@dataclass(frozen=True)
class YearRegexes:
    four_digit_year_regex: str
    all_digit_year_regex: str
    two_to_four_digit_year_map: dict[str, str]


def first_not_none[T](values: Iterable[T | None]) -> T | None:
    return next((x for x in values if x is not None), None)


def make_year_regexes(max_years_behind: int, max_years_ahead: int) -> YearRegexes:
    year_now = datetime.datetime.now(tz=datetime.UTC).astimezone().year
    year_range_list = [
        str(year)
        for year in range(year_now - max_years_behind, year_now + max_years_ahead)
    ]
    two_digit_years = [year_str[-2:] for year_str in year_range_list]
    return YearRegexes(
        four_digit_year_regex=r"(" + "|".join(year_range_list) + r")",
        all_digit_year_regex=r"(" + "|".join(year_range_list + two_digit_years) + r")",
        two_to_four_digit_year_map={
            year_str[-2:]: year_str for year_str in year_range_list
        },
    )


def strip_ordinal_suffix(day_str: str) -> str:
    """
    Strip ordinal suffix from day string if it's valid.

    Args:
        day_str: Day string that may include ordinal suffix (e.g., "21st", "2nd")

    Returns:
        Day string without ordinal suffix if valid, original string if invalid

    """
    match = re.match(r"^(\d+)(st|nd|rd|th)$", day_str, re.IGNORECASE)
    if not match:
        return day_str

    num, suffix = match.groups()
    suffix = suffix.lower()

    # Validate the ordinal is correct
    # Special cases: 11, 12, 13 always use 'th'
    if len(num) >= 2 and num[-2:] in ("11", "12", "13"):  # noqa: PLR2004
        if suffix == "th":
            return num
        return day_str  # Invalid ordinal, keep as-is

    # Check last digit
    last_digit_suffix = {"1": "st", "2": "nd", "3": "rd"}
    expected_suffix = last_digit_suffix.get(num[-1], "th")

    if suffix == expected_suffix:
        return num
    return day_str  # Invalid ordinal, keep as-is


def _month_name_to_digit(month_name: str) -> int:
    """Convert a month name to its 1-based digit, trying system locale then English."""
    month_lower = month_name.lower()
    for names in (
        [s.lower() for s in calendar.month_abbr],
        [s.lower() for s in calendar.month_name],
        [s.lower() for s in _ENGLISH_MONTH_ABBRS],
        [s.lower() for s in _ENGLISH_MONTH_NAMES],
    ):
        if month_lower in names:
            return names.index(month_lower)
    msg = f"Unrecognised month name: {month_name!r}"
    raise ValueError(msg)


def create_regex(four_digit_year_regex: str, all_digit_year_regex: str) -> str:
    # Combine locale-specific month names with English so that both are always
    # recognised. dict.fromkeys preserves order while deduplicating.
    locale_names = list(calendar.month_name[1:13])
    locale_abbrs = list(calendar.month_abbr[1:13])
    all_names = list(dict.fromkeys(locale_names + _ENGLISH_MONTH_NAMES[1:]))
    all_abbrs = list(dict.fromkeys(locale_abbrs + _ENGLISH_MONTH_ABBRS[1:]))
    month_names_only = (
        "|".join(map(insensitiveize, all_names))
        + "|"
        + "|".join(map(insensitiveize, all_abbrs))
    )
    month = r"(0[1-9]|1[012]|[1-9](?!\d)|" + month_names_only + ")"
    day = r"(0[1-9]|[12]\d|3[01]|[1-9](?!\d))"
    # Day with optional ordinal suffix - only used with month names
    day_with_ordinal = r"(0[1-9]|[12]\d|3[01]|[1-9](?!\d))(?:st|nd|rd|th)?"
    hour = r"([01]\d|2[0123])"
    minute = second = r"[012345]\d"

    date_separator = r"[-_.\s]?"
    ymd_separator_first = r"(?P<ymdsep>" + date_separator + r")"
    ymd_separator_following = r"(?P=ymdsep)"
    dmy_separator_first = r"(?P<dmysep>" + date_separator + r")"
    dmy_separator_following = r"(?P=dmysep)"
    dmytdy_separator_first = r"(?P<dmytdysep>" + date_separator + r")"
    dmytdy_separator_following = r"(?P=dmytdysep)"
    my_separator = date_separator
    hms_separator_first = r"(?P<hmssep>[-_.\s]?)"
    hms_separator_following = r"(?P=hmssep)"
    date_time_separator = r"([-_T\s]|\sat\s|,\s)"

    ymd_style = (
        r"(?P<year1>"
        + four_digit_year_regex
        + r")"
        + ymd_separator_first
        + r"(?P<month1>"
        + month
        + r")"
        + r"("
        + ymd_separator_following
        + r"(?P<day1>"
        + day
        + r"))?"
    )

    dmy_style = (
        r"(?P<day2>"
        + day
        + r")"
        + dmy_separator_first
        + r"(?P<month2>"
        + month
        + r")"
        + dmy_separator_following
        + r"(?P<year2>"
        + four_digit_year_regex
        + r")"
    )

    dmy_style_twodigityears_months_in_name_only = (
        r"(?P<day4>"
        + day_with_ordinal
        + r")"
        + dmytdy_separator_first
        + r"(?P<month4>"
        + month_names_only
        + r")"
        + dmytdy_separator_following
        + r"(?P<year4>"
        + all_digit_year_regex
        + r")"
    )

    my_style_months_in_name_only = (
        r"(?P<month3>"
        + month_names_only
        + r")"
        + my_separator
        + r"(?P<year3>"
        + four_digit_year_regex
        + r")"
    )

    return (
        r"^(?P<prefix>.*?)[-_]?"
        + r"("
        + ymd_style
        + r"|"
        + dmy_style
        + r"|"
        + dmy_style_twodigityears_months_in_name_only
        + r"|"
        + my_style_months_in_name_only
        + r")"
        + r"("
        + date_time_separator
        + r"(?P<hour>"
        + hour
        + r")"
        + (r"(" + hms_separator_first + r"(?P<minute>" + minute + r")")
        + (r"(" + hms_separator_following + r"(?P<second>" + second + r"))?)?)?")
        + r"(?P<suffix>.*)$"
    )


def datetime_prefix(  # noqa: C901
    args: Args, non_extension: str, filename: Path, year_regexes: YearRegexes
) -> str:
    def replacement(matchobj: re.Match[str]) -> str:
        logger.debug(f"replacement() called, matchobj = {matchobj}")

        year = str(
            first_not_none(
                [
                    matchobj.group("year1"),
                    matchobj.group("year2"),
                    matchobj.group("year3"),
                    matchobj.group("year4"),
                ]
            )
        )
        month = str(
            first_not_none(
                [
                    matchobj.group("month1"),
                    matchobj.group("month2"),
                    matchobj.group("month3"),
                    matchobj.group("month4"),
                ]
            )
        )
        day = first_not_none(
            [matchobj.group("day1"), matchobj.group("day2"), matchobj.group("day4")]
        )

        if len(year) == 2:  # noqa: PLR2004
            year = year_regexes.two_to_four_digit_year_map[year]

        if not month.isdigit():
            month = str(_month_name_to_digit(month))

        if len(month) == 1:
            month = month.zfill(2)

        # Strip ordinal suffix from day if present and valid
        if day is not None:
            stripped_day = strip_ordinal_suffix(day)
            # If day contains an ordinal suffix but stripping didn't change it,
            # it means the ordinal was invalid - reject this match
            if re.search(r"(st|nd|rd|th)$", day, re.IGNORECASE) and stripped_day == day:
                raise _InvalidOrdinalError
            day = stripped_day
            if len(day) == 1:
                day = day.zfill(2)

        replace_value = (
            year
            + "-"
            + month
            + (("-" + day) if day is not None else "")
            + (
                ("T" + matchobj.group("hour"))
                if matchobj.group("hour") is not None
                else ""
            )
            + (
                ("-" + matchobj.group("minute"))
                if matchobj.group("minute") is not None
                else ""
            )
            + (
                ("-" + matchobj.group("second"))
                if matchobj.group("second") is not None
                else ""
            )
        )

        if not args.discard_existing_name:
            replace_value = replace_value + (
                (
                    ("-" + matchobj.group("prefix"))
                    if matchobj.group("prefix") != ""
                    else ""
                )
                + (matchobj.group("suffix") if matchobj.group("suffix") != "" else "")
            )

        logger.debug(f"replacement() returned: {replace_value}")
        return replace_value

    regex_str = create_regex(
        year_regexes.four_digit_year_regex, year_regexes.all_digit_year_regex
    )

    logger.debug(f"Complete regex used against {non_extension}: {regex_str}")

    try:
        (newname, number_of_subs) = re.subn(regex_str, replacement, non_extension)
    except _InvalidOrdinalError:
        number_of_subs = 0
        newname = non_extension

    if number_of_subs > 1:
        msg = "Number of subs should be less than 1"
        raise ValueError(msg)

    if number_of_subs == 0:
        logger.debug("Didn't find date or time")

        pdf_date = get_pdf_creation_date(filename)
        timetouse = (
            pdf_date
            if pdf_date is not None
            else get_timetouse(args.time_option, filename)
        )

        newname_with_dash_if_needed = (
            ("-" + newname) if not args.discard_existing_name else ""
        )

        local_timetouse = timetouse.astimezone()
        if args.add_time:
            newname = (
                local_timetouse.strftime("%Y-%m-%dT%H-%M-%S")
                + newname_with_dash_if_needed
            )
        else:
            newname = local_timetouse.strftime("%Y-%m-%d") + newname_with_dash_if_needed

    return newname
