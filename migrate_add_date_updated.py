from app import app, db, Milestone
from utils import sqlite_connection

with app.app_context(), sqlite_connection(db) as conn:
    table = Milestone.__table__.name
    cur = conn.cursor()
    # check if column exists
    cur.execute("PRAGMA table_info(%s)" % table)
    cols = [r[1] for r in cur.fetchall()]
    if 'date_updated' not in cols:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN date_updated DATETIME")
        print('Added date_updated column')
    else:
        print('date_updated already exists')
    # sync values where null
    cur.execute(f"UPDATE {table} SET date_updated = date_created WHERE date_updated IS NULL")
    print('Synchronized date_updated values')
