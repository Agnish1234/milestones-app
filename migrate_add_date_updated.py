from app import app, db, Milestone
import sqlite3
from datetime import datetime
import os

with app.app_context():
    db_path = db.engine.url.database
    table = Milestone.__table__.name
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # check if column exists
    cur.execute("PRAGMA table_info(%s)" % table)
    cols = [r[1] for r in cur.fetchall()]
    if 'date_updated' not in cols:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN date_updated DATETIME")
        conn.commit()
        print('Added date_updated column')
    else:
        print('date_updated already exists')
    # sync values where null
    cur.execute(f"UPDATE {table} SET date_updated = date_created WHERE date_updated IS NULL")
    conn.commit()
    print('Synchronized date_updated values')
    conn.close()
