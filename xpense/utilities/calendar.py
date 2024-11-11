import datetime
from math import copysign


def get_sign(x):
    return int(copysign(1, x))


def convert_string_into_datetime(datetime_str: str) -> datetime.datetime:
    """Converts string of form 2024-02-16 00:00:00"""
    return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


def convert_datetime_to_string(dt: datetime.datetime) -> str:
    """Converts a datetime object to a string of form 2024-02-16 00:00:00"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")
