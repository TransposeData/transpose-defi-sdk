from datetime import timezone 
from dateutil import parser


def to_iso(timestamp: str) -> str:
    """
    Parses a timestamp string into a valid ISO-8601 string.

    :param timestamp: The timestamp to parse.
    :return: The parsed timestamp.
    """

    dt = parser.parse(timestamp)
    if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')