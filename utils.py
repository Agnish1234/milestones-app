"""Shared utilities for the milestones app."""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta

# Fixed IST (UTC+05:30) timezone used for all stored timestamps.
LOCAL_TZ = timezone(timedelta(hours=5, minutes=30))


def now_ist():
    """Return the current time in the fixed IST timezone."""
    return datetime.now(LOCAL_TZ)


@contextmanager
def sqlite_connection(db):
    """Yield a raw sqlite3 connection to the app's database.

    Commits on successful exit and always closes the connection. Must be used
    within an active Flask app context so ``db.engine`` is available.
    """
    conn = sqlite3.connect(db.engine.url.database)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
