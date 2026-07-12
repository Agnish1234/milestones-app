from app import app, db, Milestone
import sqlite3
from datetime import datetime, timezone, timedelta

# fixed IST timezone
LOCAL_TZ = timezone(timedelta(hours=5, minutes=30))

with app.app_context():
    db_path = db.engine.url.database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # read existing rows
    cur.execute(f"SELECT id, date_created, date_updated FROM {Milestone.__table__.name}")
    rows = cur.fetchall()
    for r in rows:
        id_, created, updated = r
        # SQLite stores as text; if None skip
        if created:
            try:
                created_dt = datetime.fromisoformat(created)
            except (ValueError, TypeError) as exc:
                print(f"Skipping row {id_}: could not parse date_created={created!r}: {exc}")
            else:
                created_ist = created_dt.astimezone(LOCAL_TZ).isoformat()
                cur.execute(f"UPDATE {Milestone.__table__.name} SET date_created=? WHERE id=?", (created_ist, id_))
        if updated:
            try:
                updated_dt = datetime.fromisoformat(updated)
            except (ValueError, TypeError) as exc:
                print(f"Skipping row {id_}: could not parse date_updated={updated!r}: {exc}")
            else:
                updated_ist = updated_dt.astimezone(LOCAL_TZ).isoformat()
                cur.execute(f"UPDATE {Milestone.__table__.name} SET date_updated=? WHERE id=?", (updated_ist, id_))
    conn.commit()
    conn.close()
    print('Converted timestamps to IST (string ISO format)')
