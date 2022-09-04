from pymongo import MongoClient
import os


# Just testing for now.  My container does NOT want to work with mongodb
def tryConnecting():
    client = MongoClient(f'mongodb://{os.environ.get("MONGODB_USERNAME")}:{os.environ.get("MONGODB_PASSWORD")}@localhost:27017/')
