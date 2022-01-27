from fpldb.logger.logger import logger

class Datastore:
    store = {}

    @staticmethod
    def add(key, value, expiry = None):
        Datastore.store[key] = {}
        Datastore.store[key]['data'] = value
        Datastore.store[key]['expiry'] = expiry

    @staticmethod
    def get(key):
        if key in Datastore.store:
            return Datastore.store[key]
        return None

    @staticmethod
    def cleanUp():
        Datastore.store = {}




