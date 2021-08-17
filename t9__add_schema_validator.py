from collections import OrderedDict

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["pymongo"]

schema = {"$jsonSchema": {"required": ["name", "value"]}}

col = db["t0"]
col.drop()
col.insert_one({"name": "n1", "value": 2})

query = [("collMod", "t0"), ("validator", schema), ("validationLevel", "strict")]
res = db.command(OrderedDict(query))
print(res)

col.insert_one({"name": "n1", "value": 2})
# insert ok

col.insert_one({"name": "n2"})
# this fails with the error
