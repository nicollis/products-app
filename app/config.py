import os

class Config:
    """
    A class for storing configuration variables for the Products API.

    Attributes:
        MONGO_USERNAME (str): The username for the MongoDB database.
        MONGO_PASSWORD (str): The password for the MongoDB database.
        MONGO_HOST (str): The host URL for the MongoDB database.
        MONGO_DB (str): The name of the MongoDB database.
        ELASTICSEARCH_HOST (str): The host URL for the Elasticsearch database.
        ELASTICSEARCH_USERNAME (str): The username for the Elasticsearch database.
        ELASTICSEARCH_PASSWORD (str): The password for the Elasticsearch database.
    """
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    MONGO_DB = os.environ.get('MONGO_DB')

    ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST')
    ELASTICSEARCH_USERNAME = os.environ.get('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD = os.environ.get('ELASTICSEARCH_PASSWORD')