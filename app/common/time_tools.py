from datetime import datetime, timezone


def now_timestamp():
    return int(datetime.now(timezone.utc).timestamp())
