from datetime import datetime, timezone, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
LOCAL_TZ = timezone(timedelta(hours=5, minutes=30))


class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(LOCAL_TZ))
    date_updated = db.Column(db.DateTime, default=lambda: datetime.now(LOCAL_TZ), onupdate=lambda: datetime.now(LOCAL_TZ))

    def __repr__(self) -> str:
        return f'<Milestone {self.id} - {self.title}>'

    def get_timestamp(self):
        return datetime.now(LOCAL_TZ)
