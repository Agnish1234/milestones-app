from flask_sqlalchemy import SQLAlchemy

from utils import now_ist

db = SQLAlchemy()


class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=now_ist)
    date_updated = db.Column(db.DateTime, default=now_ist, onupdate=now_ist)

    def __repr__(self) -> str:
        return f'<Milestone {self.id} - {self.title}>'

    def get_timestamp(self):
        return now_ist()
