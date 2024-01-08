from datetime import datetime
from typing import Final

import pytz

PST_TIMEZONE: Final = pytz.timezone(zone="US/Pacific")
UTC_TIMEZONE: Final = pytz.utc


class DTConverter:
    @staticmethod
    def str_to_utc_dt(dt: str) -> datetime:
        """Converts a datetime string to a UTC datetime object.

        Args:
            dt: The datetime string.

        Returns:
            A UTC datetime object.
        """

        patterns: list[str] = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%d %H:%M:%S",
        ]
        for pattern in patterns:
            try:
                return UTC_TIMEZONE.localize(dt=datetime.strptime(dt, pattern).replace(microsecond=0), is_dst=None)
            except ValueError:
                pass
        raise ValueError(f"Invalid date format for {dt}")

    @staticmethod
    def str_to_pst_dt(dt: str) -> datetime:
        """Converts a datetime string to a UTC datetime object.

        Args:
            dt: The datetime string.

        Returns:
            A UTC datetime object.
        """

        patterns: list[str] = [
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%d %H:%M:%S",
        ]
        for pattern in patterns:
            try:
                return PST_TIMEZONE.localize(dt=datetime.strptime(dt, pattern).replace(microsecond=0), is_dst=None)
            except ValueError:
                pass
        raise ValueError(f"Invalid date format for {dt}")

    @staticmethod
    def utc_now() -> datetime:
        """Returns the current UTC datetime.

        Returns:
            A UTC datetime object.
        """

        return UTC_TIMEZONE.localize(dt=datetime.utcnow(), is_dst=None)
    
        
    @staticmethod
    def dt_to_pst_dt(dt: datetime) -> datetime:
        """Converts a datetime to a PST datetime object.

        Args:
            dt: The datetime.

        Returns:
            A PST datetime object.
        """

        try:
            return PST_TIMEZONE.localize(dt=dt.replace(microsecond=0), is_dst=None)
        except ValueError:
            pass
        raise ValueError(f"Invalid date format for {dt}")

    @staticmethod
    def utc_to_pst(dt: datetime) -> datetime:
        """Casts a UTC datetime to PST datetime using localize function of pytz.timezone module.

        Args:
            dt: The UTC datetime.

        Returns:
            A datetime object in PST format.
        """

        return PST_TIMEZONE.localize(dt)

    @staticmethod
    def utc_to_pst_with_tz(dt: datetime) -> datetime:
        """Casts a UTC datetime to PST datetime using replace function of datetime module.

        Args:
            dt: The UTC datetime.

        Returns:
            A datetime object in PST format.
        """

        return dt.astimezone(PST_TIMEZONE)

    @staticmethod
    def pst_to_utc(dt: datetime) -> datetime:
        """Casts a PST datetime to UTC datetime.

        Args:
            dt: The PST datetime.

        Returns:
            A datetime object in UTC format.
        """

        return dt.astimezone(UTC_TIMEZONE)

    @staticmethod
    def dt_to_iso8601(dt: datetime) -> str:
        """Casts a datetime to ISO 8601.

        Args:
            dt: The datetime object.

        Returns:
            A string in ISO 8601 format.
        """

        return dt.isoformat()

    @staticmethod
    def dt_to_str(dt: datetime) -> str:
        """Casts a datetime to string.
        Args:
            dt: The datetime object.

        Returns:
            A string in `%Y-%m-%d %H:%M:%S` format.
        """

        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def timestamp_now() -> int:
        """Returns the current UTC datetime in timestamp format.

        Returns:
            A timestamp.
        """

        return int(UTC_TIMEZONE.localize(dt=datetime.utcnow(), is_dst=None).timestamp())
