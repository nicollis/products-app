from flask import Blueprint, abort, jsonify, request
from app import mongo, elastic
from app.models.product import Product
from app.services.analytics_service import AnalyticsService

products_bp = Blueprint('products', __name__)

def get_products():
    """
    Returns all products in the database.

    Returns:
        A list of dictionaries, each representing a product.
    """
    result = Product.get_all()
    return jsonify([p.to_dict() for p in result])

def get_product(product_id):
    """
    Returns a product with the given ID.

    Args:
        product_id: The ID of the product to retrieve.

    Returns:
        A dictionary representing the product.
    """
    product = Product.get_by_id(product_id)
    return jsonify(product.to_dict())

def create_product():
    """
    Creates a new product.

    Returns:
        A dictionary containing the ID of the newly created product.
    """
    try:
        product = Product.from_request(request.json)
        product_id = product.save()
        return jsonify({"id": product_id}), 201
    except ValueError as e:
        abort(400, description=str(e))

def update_product(product_id):
    """
    Updates an existing product.

    Args:
        product_id: The ID of the product to update.

    Returns:
        A dictionary indicating whether the product was updated or not.
    """
    # Get the existing product
    existing_product = Product.get_by_id(product_id)
    if not existing_product:
        abort(404)

    # Update only the fields that are provided in the request
    for k,v in request.json.items():
        if hasattr(existing_product, k):
            setattr(existing_product, k, v)

    # Update the product
    if existing_product.update():
        return jsonify({"result": "updated"})
    else:
        return jsonify({"result": "not modified"})

def delete_product(product_id):
    """
    Deletes a product with the given ID.

    Args:
        product_id: The ID of the product to delete.

    Returns:
        A dictionary indicating whether the product was deleted or not.
    """
    result = Product.delete(product_id)
    return jsonify({'result': result})

def search_products():
    """
    Searches for products based on a query string.

    Returns:
        A list of dictionaries, each representing a product.
    """
    query = request.args.get('query')
    if not query:
        abort(400, description="Query parameter is required")

    result = Product.search(query)
    return jsonify(result)

def analytics():
    """
    Generates a report of product analytics.

    Returns:
        A dictionary containing the product analytics report.
    """
    return jsonify(AnalyticsService.generate_product_report())

# Define the routes for the products blueprint
products_bp.add_url_rule('/products', 'get_products', get_products, methods=['GET'])
products_bp.add_url_rule('/products/<product_id>', 'get_product', get_product, methods=['GET'])
products_bp.add_url_rule('/products', 'create_product', create_product, methods=['POST'])
products_bp.add_url_rule('/products/<product_id>', 'update_product', update_product, methods=['PUT'])
products_bp.add_url_rule('/products/<product_id>', 'delete_product', delete_product, methods=['DELETE'])
products_bp.add_url_rule('/products/search', 'search_products', search_products, methods=['GET'])
products_bp.add_url_rule('/products/analytics', 'analytics', analytics, methods=['GET'])
