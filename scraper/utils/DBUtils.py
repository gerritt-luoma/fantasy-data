from pymongo import MongoClient
import os

def getDataBase():
    db = None
    try:
        client = MongoClient(f'mongodb://{os.getenv("MONGODB_USERNAME")}:{os.getenv("MONGODB_PASSWORD")}@mongoservice:27017/?authSource=admin')
        db = client.fantasy_data
    except:
        print('failed to connect to db')
    return db

def writeToDatabase(week, data):
    db = getDataBase()
    collection = db[f'week_{week}']

    try:
        collection.insert_many(data)
    except:
        print('failed to write to database')