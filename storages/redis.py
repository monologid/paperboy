from interfaces.storage import StorageInterface
from redis import Redis
import config
import logging


class RedisStorage(StorageInterface):
    """
    Redis storage class
    """
    host = None
    port = None
    db = None
    client = None

    def __init__(self):
        self.host = config.Config.REDIS_HOST
        self.port = config.Config.REDIS_PORT
        self.db = config.Config.REDIS_DB

    def connect(self):
        self.client = Redis(host=self.host, port=self.port, db=self.db)
        return self

    def get(self, key):
        try:
            result = self.client.get(key)
            return result
        except Exception as e:
            logging.exception(f"Something went wrong when retrieving data, key={key}")
            return None

    def set(self, key, value):
        try:
            self.client.set(key, value)
            return True
        except Exception as e:
            logging.exception(f"Something went wrong when writing data, key={key}")
            return False

    def delete(self, key):
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logging.exception(f"Something went wrong when writing data, key={key}")
            return False
