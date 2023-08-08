from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union
from bson import ObjectId

from app import mongo, elastic
from app.protocols.requestable import Requestable

@dataclass
class Product(Requestable):
    """
    A class representing a product.

    Attributes:
    _id (str): The unique identifier of the product.
    name (str): The name of the product.
    category (str): The category of the product.
    _price (int): The price of the product in cents.
    quantity (str): The quantity of the product.
    description (str): The description of the product.
    """

    _id: str
    name: str 
    category: str 
    _price: int # Store price in cents 
    quantity: str 
    description: str 

    @property
    def price(self) -> float:
        return round(self._price / 100, 2)
    
    @price.setter
    def price(self, value: Union[float, int]) -> None:
        self._price = int(value * 100)

    @classmethod
    def from_request(cls, data: dict) -> Product:
        """
        Creates a new Product instance from a request data dictionary.

        Args:
        data (dict): The request data dictionary.

        Returns:
        Product: A new Product instance.
        """
        name = data.get('name')
        category = data.get('category')
        price = data.get('price') * 100
        quantity = data.get('quantity')
        description = data.get('description')
        if not all([name, category, price, quantity, description]):
            raise ValueError('Missing required fields')
        return cls(None, name, category, price, quantity, description)
    
    @classmethod
    def from_mongo(cls, data: dict) -> Product:
        """
        Creates a new Product instance from a MongoDB data dictionary.

        Args:
        data (dict): The MongoDB data dictionary.

        Returns:
        Product: A new Product instance.
        """
        return cls(
            _id=str(data['_id']),
            name=data['ProductName'],
            category=data['ProductCategory'],
            _price=data['Price'],
            quantity=data['AvailableQuantity'],
            description=data['ProductDescription']
        )
    
    def to_dict(self):
        """
        Returns a dictionary representation of the Product instance.

        Returns:
        dict: A dictionary representation of the Product instance.
        """
        return {
            'id': self._id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'description': self.description
        }

    def save(self) -> str:
        """
        Saves the Product instance to the database.

        Returns:
        str: The unique identifier of the saved Product instance.
        """
        self._id = str(mongo.db.products.insert_one({
            "ProductName": self.name,
            "ProductCategory": self.category,
            "Price": self._price,
            "AvailableQuantity": self.quantity,
            "ProductDescription": self.description
        }).inserted_id)

        self._elasticsearch_save()

        return str(self._id)

    @staticmethod
    def get_all() -> list[Product]:
        """
        Returns a list of all Product instances in the database.

        Returns:
        list[Product]: A list of all Product instances in the database.
        """
        products = mongo.db.products.find()
        result = []
        for product in products:
            result.append(Product.from_mongo(product))
        return result

    @staticmethod
    def get_by_id(product_id: str) -> Optional[Product]:
        """
        Returns the Product instance with the given identifier.

        Args:
        product_id (str): The identifier of the Product instance.

        Returns:
        Optional[Product]: The Product instance with the given identifier, or None if not found.
        """
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        if product is None:
            return None
        product = Product.from_mongo(product)
        return product

    def update(self: str) -> bool:
        """
        Updates the Product instance in the database.

        Returns:
        bool: True if the Product instance was updated, False otherwise.
        """
        result = mongo.db.products.update_one(
            {"_id": ObjectId(self._id)},
            {"$set": {
                "ProductName": self.name,
                "ProductCategory": self.category,
                "Price": self._price,
                "AvailableQuantity": self.quantity,
                "ProductDescription": self.description
            }}
        )

        self._elasticsearch_save()

        return result.modified_count > 0

    @staticmethod
    def delete(product_id):
        """
        Deletes the Product instance with the given identifier from the database.

        Args:
        product_id (str): The identifier of the Product instance.

        Returns:
        bool: True if the Product instance was deleted, False otherwise.
        """
        mongo_result = mongo.db.products.delete_one({"_id": ObjectId(product_id)})
        elastic_result = elastic.delete(index="products", id=str(product_id))
        return mongo_result.deleted_count > 0 and elastic_result["result"] == "deleted"

    @staticmethod
    def search(query: str) -> list[Product]:
        """
        Searches for Product instances in the database with the given query.

        Args:
        query (str): The search query.

        Returns:
        list[Product]: A list of Product instances that match the search query.
        """
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
        """
        Returns the total number of Product instances in the database.

        Returns:
        int: The total number of Product instances in the database.
        """
        return mongo.db.products.count_documents({})
    
    # private

    def _elasticsearch_save(self):
        """
        Saves the Product instance to Elasticsearch.

        Returns:
        dict: The Elasticsearch response.
        """
        doc = {
            "description": self.description,
            "word_count": len(self.description.split(" ")),
        }
        return elastic.index(index="products", id=self._id, document=doc)