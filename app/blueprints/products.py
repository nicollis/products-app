from flask import Blueprint, abort, jsonify, request
from app import mongo, elastic
from app.models.product import Product
from app.services.analytics_service import AnalyticsService

products_bp = Blueprint('products', __name__)

# GET /products
@products_bp.route("/products", methods=["GET"])
def get_products():
    result = Product.get_all()
    return jsonify([p.to_dict() for p in result])

# GET /products/<product_id>
@products_bp.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.get_by_id(product_id)
    return jsonify(product.to_dict())

# POST /products
@products_bp.route("/products", methods=["POST"])
def create_product():
    try:
        product = Product.from_request(request)
        product_id = product.save()
        return jsonify({"id": product_id}), 201
    except ValueError as e:
        abort(400, description=str(e))

# PUT /products/<product_id>
@products_bp.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
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

# DELETE /products/<product_id>
@products_bp.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    result = Product.delete(product_id)
    return jsonify({'result': result})


# GET /products/search?query=<query>
@products_bp.route("/products/search", methods=["GET"])
def search_products():
    query = request.args.get('query')
    if not query:
        abort(400, description="Query parameter is required")

    result = Product.search(query)
    return jsonify(result)

# GET /products/analytics
@products_bp.route("/products/analytics", methods=["GET"])
def analytics():
    return jsonify(AnalyticsService.generate_product_report())