# from flask import Blueprint, jsonify, request
# from app.models.user import Product
# from app import db
# bp = Blueprint('products', __name__)

# @bp.route('/product', methods=['POST'])
# def add_product():
#     data = request.get_json()  # Get the JSON data from the request
    
#     # Get data from the request
#     name = data.get('name')
#     # description = data.get('description')
#     price = data.get('price')
#     stock_quantity = data.get('stock_quantity')
    
#     # Check if all fields are provided
#     if not name or not price :
#         return jsonify({"message": "All fields are required!"}), 400
    
#     # Create a new product
#     new_product = Product(
#         name=name,
#         # description=description,
#         price=price,
#         # stock_quantity=stock_quantity
#     )
    
#     # Add product to the database
#     db.session.add(new_product)
#     db.session.commit()
    
#     return jsonify({"message": "Product added successfully!"}), 201

# @bp.route('/product', methods=['GET'])
# def get_products():
#     # Fetch all products from the database
#     products = Product.query.all()
    
#     # If no products exist, return an empty list
#     if not products:
#         return jsonify({"message": "No products found"}), 404
    
#     # Serialize the products into a list of dictionaries
#     products_data = [
#         {
#             "id": product.id,
#             "name": product.name,
#             "price": product.price,
#             "stock_quantity": product.stock_quantity,  # Assuming you have this field in the model
#         }
#         for product in products
#     ]
    
#     return jsonify({"products": products_data}), 200