"""Date helpers for orgplan."""

import datetime


class DateService:
    def current_year_month(self, today=None):
        if today is None:
            today = datetime.date.today()
        return today.year, today.month

    def parse_year_month(self, value):
        if not value or "-" not in value:
            raise ValueError("Expected YYYY-MM")
        year_str, month_str = value.split("-", 1)
        year = int(year_str)
        month = int(month_str)
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")
        return year, month
