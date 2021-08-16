from datetime import datetime
from enum import Enum
from typing import List

from bson import ObjectId
from prettyprinter import cpprint, install_extras
from pydantic import BaseModel, Field
from pymongo import MongoClient

install_extras(["dataclasses"])

client = MongoClient("mongodb://localhost:27017")
db = client["pymongo"]
col = db["t4"]

col.delete_many({})


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class MongoModel(BaseModel):
    id: ObjectIdStr = Field(None, alias="_id")

    def new_document(self) -> dict:
        obj = self.dict()
        del obj["id"]
        return obj


class Address(BaseModel):
    country: str
    zip: int


class DataStatus(str, Enum):
    new = "new"
    ok = "ok"
    error = "error"


class Data(MongoModel):
    name: str
    value: int
    address: Address
    status: DataStatus = Field(default=DataStatus.new)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


col.insert_one(Data(name="n1", value=1, address=Address(country="USA", zip=123321), tags=["vv", "ggg"]).new_document())

res = col.find_one({"name": "n1"})
print(Data(**res))

col.insert_many(
    [
        d.new_document()
        for d in [
            Data(name="n2", value=2, address=Address(country="France", zip=3334)),
            Data(name="n3", value=3, address=Address(country="Italy", zip=77334), status=DataStatus.error),
        ]
    ]
)

res = list(col.find().sort("name", -1))
cpprint(res)
cpprint([Data(**x) for x in res])

cpprint({"error_data": list(col.find({"status": DataStatus.error}))})


class MongoModelIntId(MongoModel):
    id: int = Field(None, alias="_id")

    def new_document(self) -> dict:
        obj = self.dict()
        return obj


class Data2(MongoModelIntId):
    name: str


data2 = Data2(_id=1, name="a")
print(data2)
exit

col2 = db["t4_2"]

col2.delete_many({})
col2.insert_one(data2.new_document())

print(col2.find_one({}))

client.close()
