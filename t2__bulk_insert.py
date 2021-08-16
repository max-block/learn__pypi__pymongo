from datetime import datetime

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["pymongo"]
col = db["t2"]

col.delete_many({})

res = col.insert_many(
    [
        {"name": "n1", "value": 1, "created_at": datetime.utcnow()},
        {"name": "n2", "value": 2, "created_at": datetime.utcnow()},
        {"name": "n3", "value": 3, "created_at": datetime.utcnow()},
    ]
)

print(res.inserted_ids)
# [ObjectId('5f03697d8511d594792a4928'), ObjectId('5f03697d8511d594792a4929'), ObjectId('5f03697d8511d594792a492a')]
