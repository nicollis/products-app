from flask import Flask
from flask_pymongo import MongoClient
from elasticsearch import Elasticsearch

mongo: MongoClient = None
elastic: Elasticsearch = None

def create_app():
    global mongo, elastic

    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize database connections
    mongo_client = MongoClient(
        f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@{app.config['MONGO_HOST']}/")
    mongo = mongo_client[app.config['MONGO_DB']]

    if app.config['ELASTICSEARCH_USERNAME'] and app.config['ELASTICSEARCH_PASSWORD']:
        elastic = Elasticsearch([app.config['ELASTICSEARCH_HOST']], http_auth=(app.config['ELASTICSEARCH_USERNAME'], app.config['ELASTICSEARCH_PASSWORD']))
    else:
        elastic = Elasticsearch([app.config['ELASTICSEARCH_HOST']])

    # Register blueprints
    from app.blueprints import products_bp
    app.register_blueprint(products_bp)

    return app