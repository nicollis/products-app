# Products API

Simple API that is using the following tech:
- Flask
- Docker
- Kubernetes
- MongoDB
- Elasticsearch

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)

## Installation
Two paths are available for project setup

### Docker Compose
In a terminal enter the following
1. Will start up and create the services
    - `docker compose up` 
2. Will seed the database with test values
    - `docker compose exec api python seed.py`

### Kubernetes
In a terminal enter the following


1. Create secrets for MongoDB 
    - `kubectl create secret generic mongodb-secret --from-literal=username=root --from-literal=password=root` 
2. Starts creating the K8s cluster.
    - `helm install project-api ./helm/` 
3. Shows all pods, copy the name for the project-api pod (i.e. `products-api-59b95b696b-vtshd`)
    - `kubectl get pods` 
4. Seeds the database with test values.
    - `kubectl exec -it <pod name> -- python seed.py` 

## Usage

For convenience I have included a [Postman](https://www.postman.com) Collection of all the API endpoints. Please see the `Projects API.postman_collection.json` file for examples of the api.

## Testing

Test can be ran by executing the `run_test.py` file.

- `docker compose exec api python run_test.py`
- `kubectl exec -it <pod name> -- python run_test.py`


## API Documentation

Documentation for the project's API.