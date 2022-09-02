from pymongo import MongoClient
import os

def tryConnecting():
    client = MongoClient(f'mongodb://{os.environ.get("MONGODB_USERNAME")}:{os.environ.get("MONGODB_PASSWORD")}@localhost:27017/')