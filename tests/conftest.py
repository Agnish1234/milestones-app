import pytest

import app as app_module
from models import db, Milestone


@pytest.fixture
def app():
    """Create a fresh application instance backed by an isolated in-memory DB."""
    application = app_module.create_app()
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        WTF_CSRF_ENABLED=False,
    )

    with application.app_context():
        db.drop_all()
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_milestone(app):
    """Factory that persists a Milestone and returns it."""
    def _make(title='Sample', description='A description'):
        milestone = Milestone(title=title, description=description)
        db.session.add(milestone)
        db.session.commit()
        return milestone

    return _make
