from os import environ, path
from dotenv import load_dotenv

base_dir = path.abspath(path.dirname(__name__))
file_path = path.join(base_dir, '.env')

load_dotenv(file_path)


class Config:
    DEBUG = False

    APP = environ.get('FLASK_APP')
    ENV = environ.get('FLASK_ENV')
    HOST = environ.get('HOST')
    PORT = environ.get('PORT')
    DB_ENGINE = environ.get('DB_ENGINE')

    REDIS_HOST = environ.get('REDIS_HOST')
    REDIS_PORT = environ.get('REDIS_PORT')
    REDIS_DB = environ.get('REDIS_DB')


class Production(Config):
    pass


class Development(Config):
    DEBUT = True
