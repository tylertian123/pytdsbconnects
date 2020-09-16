import datetime
import pytz

def parse_datetime(timestamp: str) -> datetime.datetime:
    """
    Convert a datetime string from the TDSB API to a Python datetime.

    :param timestamp: The timestamp as returned by the API.
    """
    if timestamp.endswith("Z"):
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    try:
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.timezone("America/Toronto"))
    except ValueError:
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
