import importlib

import config as config_module


def _reload_config(monkeypatch, env):
    for key in ('DATABASE_URL', 'SECRET_KEY'):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(config_module).Config


def test_default_secret_key(monkeypatch):
    Config = _reload_config(monkeypatch, {})
    assert Config.SECRET_KEY == 'dev-secret-key'


def test_secret_key_from_env(monkeypatch):
    Config = _reload_config(monkeypatch, {'SECRET_KEY': 'super-secret'})
    assert Config.SECRET_KEY == 'super-secret'


def test_track_modifications_disabled(monkeypatch):
    Config = _reload_config(monkeypatch, {})
    assert Config.SQLALCHEMY_TRACK_MODIFICATIONS is False


def test_sqlite_fallback_when_no_database_url(monkeypatch):
    Config = _reload_config(monkeypatch, {})
    assert Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite:///')
    assert Config.SQLALCHEMY_DATABASE_URI.endswith('milestones.db')


def test_postgres_scheme_is_normalized(monkeypatch):
    Config = _reload_config(
        monkeypatch, {'DATABASE_URL': 'postgres://user:pw@host:5432/db'}
    )
    assert Config.SQLALCHEMY_DATABASE_URI == 'postgresql://user:pw@host:5432/db'


def test_postgresql_scheme_is_preserved(monkeypatch):
    url = 'postgresql://user:pw@host:5432/db'
    Config = _reload_config(monkeypatch, {'DATABASE_URL': url})
    assert Config.SQLALCHEMY_DATABASE_URI == url


def test_database_url_whitespace_is_stripped(monkeypatch):
    Config = _reload_config(
        monkeypatch, {'DATABASE_URL': '  postgres://user:pw@host/db  '}
    )
    assert Config.SQLALCHEMY_DATABASE_URI == 'postgresql://user:pw@host/db'


def test_non_postgres_url_used_verbatim(monkeypatch):
    url = 'mysql://user:pw@host/db'
    Config = _reload_config(monkeypatch, {'DATABASE_URL': url})
    assert Config.SQLALCHEMY_DATABASE_URI == url
