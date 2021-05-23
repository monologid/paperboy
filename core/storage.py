from config import Config
from interfaces.storage import StorageInterface
from storages.redis import RedisStorage


class Storage(StorageInterface):
    """
    Storage class
    To change storage engine according to app requirements
    """
    storage = None

    def __init__(self):
        if Config.DB_ENGINE == 'redis':
            self.storage = RedisStorage()
        else:
            self.storage = RedisStorage()

    def connect(self):
        self.storage.connect()
        return self

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value):
        return self.storage.set(key, value)

    def delete(self, key):
        return self.storage.delete(key)
