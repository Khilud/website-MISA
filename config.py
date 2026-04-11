import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


def _build_database_uri():
    raw_database_url = os.environ.get('DATABASE_URL')
    if not raw_database_url:
        return 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Some providers still expose the deprecated postgres:// scheme.
    if raw_database_url.startswith('postgres://'):
        return raw_database_url.replace('postgres://', 'postgresql://', 1)
    return raw_database_url

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError('SECRET_KEY environment variable is required.')
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True
    }
    PREFERRED_URL_SCHEME = 'https'


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False