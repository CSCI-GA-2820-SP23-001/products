"""
My Service

Describe what your service does here
"""

from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Product, Category

# Import Flask application
from . import app


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Product Demo REST API Service",
            version="1.0",
            paths=url_for("create_products", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# ADD A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product
    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)

    app.logger.info("Product with ID [%s] created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product
    This endpoint will return a Product based on its id
    """
    app.logger.info("Request for product with id: %s", product_id)
    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )
    message = product.serialize()

    app.logger.info("Returning product: %s", product.name)
    return jsonify(message), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete an existing Product
    This endpoint will delete a Product based on it's id
    """
    app.logger.info("Request to delete product with id: %s", product_id)
    product = Product.find(product_id)

    if product:
        product.delete()

    return jsonify(message="success"), status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL PRODUCTS
######################################################################
# @app.route("/products", methods=["GET"])
# def list_products():
#     """
#     Lists all products.
#     This endpoint will list all the products.
#     """
#     app.logger.info("Request to list all products.")
#     products = Product.all()
#     results = [product.serialize() for product in products]
#     app.logger.info(f"Returning {len(results)} products.")
#     response = jsonify(results), status.HTTP_200_OK
#     return response


######################################################################
# QUERY PRODUCTS
######################################################################

@app.route("/products", methods=["GET"])
def list_products():
    """
    Query products.
    This endpoint will list all related products filtered by the query.
    """
    app.logger.info("Request for product list")
    products = []

    category = request.args.get("category")
    if category:
        products = Product.find_by_category(getattr(Category, category))
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update an existing Product
    This endpoint will update a Product based on the body that is posted
    """
    app.logger.info("Request to update product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    message = product.serialize()

    app.logger.info("Product with id [%s] updated.", product.id)
    return jsonify(message), status.HTTP_200_OK


######################################################################
# LIKE A PRODUCT
######################################################################
@app.route("/products/like/<int:product_id>", methods=["PUT"])
def like_products(product_id):
    """
    Like an existing Product
    This endpoint will update total likes of a Product
    """
    app.logger.info("Request to like product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.like += 1
    product.id = product_id
    product.update()
    message = product.serialize()

    app.logger.info("Product with id [%s] liked.", product.id)
    return jsonify(message), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
