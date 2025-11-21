"""Timezone-aware datetime utilities for Second Brain."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Optional

from ..config import get_config


def get_timezone() -> ZoneInfo:
    """Get configured timezone.

    Returns:
        ZoneInfo object for the configured timezone
    """
    config = get_config()
    tz_string = config.get_timezone()
    try:
        return ZoneInfo(tz_string)
    except Exception:
        # Fallback to America/New_York if invalid timezone
        return ZoneInfo("America/New_York")


def now() -> datetime:
    """Get current datetime in configured timezone.

    Returns:
        Current datetime with timezone info
    """
    tz = get_timezone()
    return datetime.now(tz)


def utcnow() -> datetime:
    """Get current datetime in UTC.

    Returns:
        Current datetime in UTC
    """
    return datetime.now(timezone.utc)


def to_local(dt: datetime) -> datetime:
    """Convert datetime to local configured timezone.

    Args:
        dt: Datetime to convert (if naive, assumes UTC)

    Returns:
        Datetime in configured timezone
    """
    if dt.tzinfo is None:
        # Assume UTC if naive
        dt = dt.replace(tzinfo=timezone.utc)

    tz = get_timezone()
    return dt.astimezone(tz)


def to_utc(dt: datetime) -> datetime:
    """Convert datetime to UTC.

    Args:
        dt: Datetime to convert (if naive, assumes local timezone)

    Returns:
        Datetime in UTC
    """
    if dt.tzinfo is None:
        # Assume local timezone if naive
        tz = get_timezone()
        dt = dt.replace(tzinfo=tz)

    return dt.astimezone(timezone.utc)


def format_datetime(dt: datetime, fmt: Optional[str] = None) -> str:
    """Format datetime in configured timezone.

    Args:
        dt: Datetime to format
        fmt: Optional strftime format string

    Returns:
        Formatted datetime string
    """
    local_dt = to_local(dt)

    if fmt is None:
        return local_dt.isoformat()

    return local_dt.strftime(fmt)


def parse_datetime(dt_string: str) -> datetime:
    """Parse datetime string to timezone-aware datetime.

    Args:
        dt_string: ISO format datetime string

    Returns:
        Timezone-aware datetime
    """
    dt = datetime.fromisoformat(dt_string)

    if dt.tzinfo is None:
        # Assume local timezone if no timezone info
        tz = get_timezone()
        dt = dt.replace(tzinfo=tz)

    return dt
