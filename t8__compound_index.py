from pymongo import ASCENDING, DESCENDING, IndexModel, MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["pymongo"]

col = db["t0"]
col.drop()

# col.create_index([("name", DESCENDING), ("age", ASCENDING)], unique=True)
col.create_indexes([IndexModel([("name", DESCENDING), ("age", ASCENDING)], unique=True)])

col.insert_one({"name": "n1", "age": 1})
print("ok")
col.insert_one({"name": "n1", "age": 2})
print("ok")
col.insert_one({"name": "n1", "age": 1})
# pymongo.errors.DuplicateKeyError: E11000 duplicate key error collection: pymongo.t0 index: name_-1_age_1 dup key:
