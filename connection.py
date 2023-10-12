from pymongo import MongoClient
import os

import env


# def connect_mongo_team():
#     CONNECTION_STRING = os.environ['MONGODB_URL']
#     client = MongoClient(CONNECTION_STRING)
#     db_Name = client['fitsixes']
#     collection_name = db_Name["team"]
#     return collection_name
#
# def connect_mongo_team_copy():
#     CONNECTION_STRING = os.environ['MONGODB_URL']
#     client = MongoClient(CONNECTION_STRING)
#     db_Name = client['fitsixes']
#     collection_name = db_Name["team_copy"]
#     return collection_name
#
# def connect_mongo_team_code():
#     CONNECTION_STRING = os.environ['MONGODB_URL']
#     client = MongoClient(CONNECTION_STRING)
#     db_Name = client['fitsixes']
#     collection_name = db_Name["team_code"]
#     return collection_name

def connect_mongo_match():
    CONNECTION_STRING = env.MONGODB_URL
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['fitsixes']
    collection_name = db_Name["match"]
    return collection_name

# def connect_mongo_pitchcordinator():
#     CONNECTION_STRING = os.environ['MONGODB_URL']
#     client = MongoClient(CONNECTION_STRING)
#     db_Name = client['fitsixes']
#     collection_name = db_Name["pitchcordinator"]
#     return collection_name
#
# def connect_mongo_navod():
#     CONNECTION_STRING = "mongodb+srv://navod:mY3rdLUQKjV2m0VS@cluster0.dnos9jm.mongodb.net/?retryWrites=true&w=majority"
#     client = MongoClient(CONNECTION_STRING)
#     db_Name = client['fitsixes']
#     collection_name = db_Name["team"]
#     return collection_name
