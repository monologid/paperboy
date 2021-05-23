from flask import current_app as app
from redis import Redis


class RedisClient:
    host: str = None
    port: str = None
    db: int = None

    def __init__(self, host=None, port=None, db=0):
        self.host = host if host is not None else app.config.get('REDIS_HOST')
        self.port = port if port is not None else app.config.get('REDIS_PORT')
        self.db = db

    def initialize(self):
        return Redis(host=self.host, port=self.port, db=self.db)

    def get_url(self):
        return f"redis://{self.host}:{self.port}/{self.db}"
