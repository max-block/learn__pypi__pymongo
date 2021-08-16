from datetime import datetime

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["pymongo"]
col = db["t1"]

col.delete_many({})

new_id = col.insert_one({"name": "n1", "created_at": datetime.utcnow()}).inserted_id
print("new_id", new_id)

col.insert_one({"name": "n2", "created_at": datetime.utcnow()})

res = list(col.find({}))

print(res)
# [{'_id': ObjectId('5f036a36e0701bc860ad76ee'), 'name': 'n1', 'created_at': datetime.datetime(2020, 7, 6, 18, 15, 18, 711000)}, {'_id': ObjectId('5f036a36e0701bc860ad76ef'), 'name': 'n2', 'created_at': datetime.datetime(2020, 7, 6, 18, 15, 18, 711000)}] # noqa
