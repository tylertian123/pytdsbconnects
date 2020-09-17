import datetime
import pytz

TORONTO = pytz.timezone("America/Toronto")

def parse_datetime(timestamp: str) -> datetime.datetime:
    """
    Convert a datetime string from the TDSB API to a Python datetime.

    :param timestamp: The timestamp as returned by the API.
    """
    if timestamp.endswith("Z"):
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    try:
        return TORONTO.localize(datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
