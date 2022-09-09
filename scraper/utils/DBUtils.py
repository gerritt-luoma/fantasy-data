from pymongo import MongoClient
import os
import logging

class DBUtils:
    def __init__(self):
        self.db = None
        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(f'mongodb://{os.getenv("MONGODB_USERNAME")}:{os.getenv("MONGODB_PASSWORD")}@mongoservice:27017/?authSource=admin')
            self.db = self.client.fantasy_data
        except:
            logging.error('Failed to connect to database')
            logging.exception('')
            return False
        return True

    def disconnect(self):
        try:
            self.client.close()
        except:
            logging.error('Failed to close clent connection')
            logging.exception('')
        self.db = None
        self.client = None

    def writeToDatabase(self, week, data):
        collection = self.db['twentyTwo']

        try:
            collection.insert_many(data)
        except:
            logging.error(f'Failed to write week #{week} to database')
            logging.exception('')
            return False
        return True