from pymongo import MongoClient
from elasticsearch import Elasticsearch
import os

# Initialize database connections
mongo_client = MongoClient(f"mongodb://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@{os.environ.get('MONGO_HOST')}/")
mongo = mongo_client[os.environ.get('MONGO_DB')]

if os.environ.get('ELASTICSEARCH_USERNAME') and os.environ.get('ELASTICSEARCH_PASSWORD'):
    elastic = Elasticsearch([os.environ.get('ELASTICSEARCH_HOST')], http_auth=(os.environ.get('ELASTICSEARCH_USERNAME'), os.environ.get('ELASTICSEARCH_PASSWORD')))
else:
    elastic = Elasticsearch([os.environ.get('ELASTICSEARCH_HOST')])

print("Seeding the database...")

# Define the products to insert
products = [
    {
        "ProductName": "Product 1",
        "ProductDescription": "This is the first product",
        "Price": 1099,
        "ProductCategory": "tech",
        "AvailableQuantity": 10
    },
    {
        "ProductName": "Product 2",
        "ProductDescription": "This is the second product",
        "Price": 1999,
        "ProductCategory": "tech",
        "AvailableQuantity": 5
    },
    {
        "ProductName": "Product 3",
        "ProductDescription": "This is the third product",
        "Price": 599,
        "ProductCategory": "marketing",
        "AvailableQuantity": 7
    }
]

# Insert the products in MongoDB
mdb_results = mongo.db.products.insert_many(products)

# Zip the inserted IDs with the products
product_ids = [str(result) for result in mdb_results.inserted_ids]
product_data = list(zip(product_ids, products))

# Index the products in Elasticsearch
for product_id, product in product_data:
    doc = {
        "description": product["ProductDescription"],
        "word_count": len(product["ProductDescription"].split(" ")),
    }
    elastic.index(index="products", id=product_id, document=doc)
