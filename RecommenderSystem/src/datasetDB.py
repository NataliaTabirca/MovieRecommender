from pymongo import MongoClient
from bson.objectid import ObjectId

def get_database():
   CONNECTION_STRING = "mongodb+srv://natalia:natalia@cluster0.xxbanbk.mongodb.net/?retryWrites=true&w=majority"
   client = MongoClient(CONNECTION_STRING)
   return client["MovieRecommender"]


dbname = get_database()
users = dbname["Users"]
