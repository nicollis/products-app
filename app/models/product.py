from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union
from bson import ObjectId
from flask import request

from app import mongo, elastic
from app.protocols.requestable import Requestable

@dataclass
class Product(Requestable):
    _id: str
    name: str 
    category: str 
    _price: int # Store price in cents 
    quantity: str 
    description: str 

    @property
    def price(self) -> float:
        return self._price / 100
    
    @price.setter
    def price(self, value: Union[float, int]):
        self._price = int(value * 100)

    @classmethod
    def from_request(cls, req: request) -> Product:
        data = request.json
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        quantity = data.get('quantity')
        description = data.get('description')
        if not all([name, category, price, quantity, description]):
            raise ValueError('Missing required fields')
        return cls(None, name, category, price, quantity, description)
    
    @classmethod
    def from_mongo(cls, data: dict) -> Product:
        return cls(
            _id=str(data['_id']),
            name=data['ProductName'],
            category=data['ProductCategory'],
            _price=data['Price'],
            quantity=data['AvailableQuantity'],
            description=data['ProductDescription']
        )
    
    def to_dict(self):
        return {
            'id': self._id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'description': self.description
        }

    def save(self) -> str:
        self._id = str(mongo.db.products.insert_one({
            "ProductName": self.name,
            "ProductCategory": self.category,
            "Price": self.price,
            "AvailableQuantity": self.quantity,
            "ProductDescription": self.description
        }).inserted_id)

        self._elasticsearch_save()

        return str(self._id)

    @staticmethod
    def get_all() -> list[Product]:
        products = mongo.db.products.find()
        result = []
        for product in products:
            result.append(Product.from_mongo(product))
        return result

    @staticmethod
    def get_by_id(product_id: str) -> Optional[Product]:
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        if product is None:
            return None
        product = Product.from_mongo(product)
        return product

    def update(self: str) -> bool:
        result = mongo.db.products.update_one(
            {"_id": ObjectId(self._id)},
            {"$set": {
                "ProductName": self.name,
                "ProductCategory": self.category,
                "Price": self.price,
                "AvailableQuantity": self.quantity,
                "ProductDescription": self.description
            }}
        )

        self._elasticsearch_save()

        return result.modified_count > 0

    @staticmethod
    def delete(product_id):
        mongo_result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})
        elastic_result = elastic.delete(index="products", id=str(product_id))
        return mongo_result.deleted_count > 0 and elastic_result["result"] == "deleted"

    @staticmethod
    def search(query: str) -> list[Product]:
        res = elastic.search(index="products", body={
            "query": {
                "match": {
                    "description": query
                }
            }
        })

        # Convert the results to a more readable format
        result = []
        for hit in res['hits']['hits']:
            result.append(Product.get_by_id(hit['_id']))
        return result

    @staticmethod
    def count_all():
        return mongo.db.products.count_documents({})
    
    # private

    def _elasticsearch_save(self):
        doc = {
            "description": self.description,
            "word_count": len(self.description.split(" ")),
        }
        return elastic.index(index="products", id=self._id, document=doc)