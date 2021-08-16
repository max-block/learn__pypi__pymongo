from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["pymongo"]
col = db["t3"]

col.delete_many({})


@dataclass
class Data:
    name: str
    value: int
    tags: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    _id: Optional[ObjectId] = None


new_data = [Data("n1", 1, ["a", "b"]), Data("n2", 2, ["c", "d"])]

col.insert_many([asdict(d) for d in new_data])

res = list(col.find().sort("name", -1))

print(res)
