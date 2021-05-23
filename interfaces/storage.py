class StorageInterface:
    def connect(self):
        """
        Create instance to the storage engine
        :return: self
        """
        pass

    def get(self, key):
        """
        Get data from storage based on key
        :param key:
        :return:
        """
        pass

    def set(self, key, value):
        """
        Set data to the storage
        :param key:
        :param value:
        :return:
        """
        pass

    def delete(self, key):
        """
        Delete existing data based on key
        :param key:
        :return:
        """
        pass
