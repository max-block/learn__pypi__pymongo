from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["pymongo"]

col = db.create_collection("t5", capped=True, size=3)
