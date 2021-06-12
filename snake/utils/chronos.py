from datetime import date

from dateutil.parser import parse as dateutil_parser


def parse_date(date_str: str) -> date:
    """Just a wrapper to avoid having to declare dateutil as a dependency in other projects."""
    return dateutil_parser(date_str).date()
