from datetime import datetime, timezone

from app import app, db, Milestone
from utils import LOCAL_TZ, sqlite_connection

with app.app_context(), sqlite_connection(db) as conn:
    table = Milestone.__table__.name
    cur = conn.cursor()
    # read existing rows
    cur.execute(f"SELECT id, date_created, date_updated FROM {table}")
    rows = cur.fetchall()
    for r in rows:
        id_, created, updated = r
        # SQLite stores as text; if None skip
        if created:
            try:
                created_dt = datetime.fromisoformat(created)
            except Exception:
                # fallback: treat as naive UTC
                created_dt = datetime.fromtimestamp(0, timezone.utc)
            created_ist = created_dt.astimezone(LOCAL_TZ).isoformat()
            cur.execute(f"UPDATE {table} SET date_created=? WHERE id=?", (created_ist, id_))
        if updated:
            try:
                updated_dt = datetime.fromisoformat(updated)
            except Exception:
                updated_dt = datetime.fromtimestamp(0, timezone.utc)
            updated_ist = updated_dt.astimezone(LOCAL_TZ).isoformat()
            cur.execute(f"UPDATE {table} SET date_updated=? WHERE id=?", (updated_ist, id_))
    print('Converted timestamps to IST (string ISO format)')
