from pymongo import MongoClient
from pymongo.errors import BulkWriteError

client = MongoClient("mongodb://localhost:27017")

db = client["pymongo"]

col = db["t6"]
col.drop()

col.create_index("name", unique=True)

new_data = [
    {"name": "n1", "value": 1},
    {"name": "n1", "value": 3},
    {"name": "n2", "value": 2},
]

try:
    col.insert_many(new_data, ordered=False)
except BulkWriteError:
    pass
print(list(col.find()))
# [{'_id': ObjectId('5f1406bc1fa6a24abed8e69d'), 'name': 'n1', 'value': 1}, {'_id': ObjectId('5f1406bc1fa6a24abed8e69e'), 'name': 'n2', 'value': 2}] # noqa
