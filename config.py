import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'
try:
    INSTANCE_DIR.mkdir(exist_ok=True)
except Exception:
    pass

class Config:
    # Never fall back to a hard-coded/predictable secret. If SECRET_KEY is not
    # provided via the environment (as it must be in production), generate a
    # random per-process key so sessions/CSRF tokens cannot be forged with a
    # known default. A production deployment should always set SECRET_KEY so the
    # value stays stable across restarts and workers.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Get DATABASE_URL and strip whitespace
    _database_url = os.environ.get('DATABASE_URL', '').strip()
    
    if _database_url:
        if _database_url.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = _database_url.replace('postgres://', 'postgresql://', 1)
        else:
            SQLALCHEMY_DATABASE_URI = _database_url
    else:
        # Use SQLite for local development
        # Convert path to string and use forward slashes for SQLite URL format
        db_path = str(INSTANCE_DIR / 'milestones.db').replace('\\', '/')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
