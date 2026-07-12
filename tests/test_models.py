from datetime import datetime, timedelta, timezone

from models import LOCAL_TZ, Milestone, db


def test_local_tz_is_ist():
    assert LOCAL_TZ.utcoffset(None) == timedelta(hours=5, minutes=30)


def test_milestone_persists_and_assigns_id(app):
    milestone = Milestone(title='Launch', description='Ship v1')
    db.session.add(milestone)
    db.session.commit()

    assert milestone.id is not None
    assert milestone.title == 'Launch'
    assert milestone.description == 'Ship v1'


def test_description_is_optional(app):
    milestone = Milestone(title='No description')
    db.session.add(milestone)
    db.session.commit()

    assert milestone.description is None


def test_default_timestamps_are_set(app):
    milestone = Milestone(title='Timed')
    db.session.add(milestone)
    db.session.commit()

    assert milestone.date_created is not None
    assert milestone.date_updated is not None


def test_repr_includes_id_and_title(app):
    milestone = Milestone(title='Reprable', description='x')
    db.session.add(milestone)
    db.session.commit()

    assert repr(milestone) == f'<Milestone {milestone.id} - Reprable>'


def test_get_timestamp_returns_ist_aware_datetime():
    milestone = Milestone(title='ts')
    stamp = milestone.get_timestamp()

    assert isinstance(stamp, datetime)
    assert stamp.utcoffset() == timedelta(hours=5, minutes=30)


def test_get_timestamp_is_close_to_now():
    milestone = Milestone(title='ts')
    stamp = milestone.get_timestamp()
    now_ist = datetime.now(timezone.utc).astimezone(LOCAL_TZ)

    assert abs((now_ist - stamp).total_seconds()) < 5
