import os
import pathlib
import secrets

# DATABASE
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL', 'postgresql://dev-user:dev-password@db:5432/dev-database')

# PATH
APP_ROOT = os.getenv('APP_ROOT', str(pathlib.Path('./').resolve()))
DATA_ROOT = os.getenv('DATA_ROOT', str(pathlib.Path('./data').resolve()))

# APP
IS_DEV = (APP_ROOT == str(pathlib.Path('./').resolve()))
API_VERSION = '1.0.0'

# JWT
SECRET_KEY = 'DEV_KEY' if IS_DEV else os.getenv('SECRET_KEY', secrets.token_urlsafe(128))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 28