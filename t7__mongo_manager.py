from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union

from bson import CodecOptions, Decimal128, ObjectId
from bson.codec_options import TypeCodec, TypeRegistry
from pydantic import BaseModel, Field
from pymongo import IndexModel
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult, UpdateResult

T = TypeVar("T", bound="MongoModel")
sort_type = Optional[List[Tuple[str, int]]]
query_type = Dict[str, Any]


class DecimalCodec(TypeCodec):
    python_type = Decimal
    bson_type = Decimal128

    def transform_python(self, value):
        return Decimal128(value)

    def transform_bson(self, value):
        return value.to_decimal()


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class Manager:
    def __init__(self, collection: Collection, model_class: Type[T]):
        self.collection = collection
        self.model_class = model_class

    def insert_one(self, obj: T) -> InsertOneResult:
        return self.collection.insert_one(obj.dict())

    def insert_many(self, objs: List[T], ordered=True) -> InsertManyResult:
        return self.collection.insert_many([obj.dict() for obj in objs], ordered=ordered)

    def get(self, pk) -> Optional[T]:
        res = self.collection.find_one({"_id": ObjectId(pk)})
        if res:
            return self.model_class(**res)

    def find(self, query: query_type, sort: sort_type = None, limit: int = 0) -> List[T]:
        return [self.model_class(**d) for d in self.collection.find(query, sort=sort, limit=limit)]

    def find_one(self, query: query_type, sort: sort_type = None) -> Optional[T]:
        res = self.collection.find_one(query, sort=sort)
        if res:
            return self.model_class(**res)

    def update_by_id(self, pk: Union[str, ObjectId], update: Dict[str, Any]) -> UpdateResult:
        return self.collection.update_one({"_id": ObjectId(pk)}, update)

    def update_one(self, query: query_type, update: Dict[str, Any]) -> UpdateResult:
        return self.collection.update_one(query, update)

    def delete_many(self, query: query_type) -> DeleteResult:
        return self.collection.delete_many(query)

    def delete_one(self, query: query_type) -> DeleteResult:
        return self.collection.delete_one(query)

    def delete_by_id(self, pk: Union[str, ObjectId]) -> DeleteResult:
        return self.collection.delete_one({"_id": ObjectId(pk)})

    def count_documents(self, query: query_type) -> int:
        return self.collection.count_documents(query)

    def exists(self, query: query_type) -> bool:
        return self.collection.count_documents(query) > 0


class ManagerMixin:
    manager: Manager


class MongoModel(ManagerMixin, BaseModel):
    id: ObjectIdStr = Field(None, alias="_id")

    @classmethod
    def init_collection(cls: Type[T], db_: Database, name: str, indexes: Optional[List[IndexModel]] = None):
        codecs = CodecOptions(type_registry=TypeRegistry([c() for c in [DecimalCodec]]))
        col = db_.get_collection(name, codecs)
        if indexes:
            col.create_indexes(indexes)
        cls.manager = Manager(col, cls)


class Data(MongoModel):
    a: str
    b: int


def main():
    Data.manager.find_one({})


if __name__ == "__main__":
    main()
