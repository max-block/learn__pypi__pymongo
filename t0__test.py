from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["pymongo"]

schema = {"$jsonSchema": {"required": ["name", "value"]}}

col = db["t0"]
col.drop()

col = db.create_collection("t0", validator=schema)

col.insert_one({"_id": 1, "name": "n1", "value": 2})
# insert ok

col.insert_one({"_id": 2, "name": "n2"})
# this fails with the error

