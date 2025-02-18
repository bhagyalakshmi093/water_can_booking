from flask import Blueprint, request, jsonify, render_template,session, flash,redirect,url_for
from werkzeug.security import generate_password_hash
from app.models.user import User
from werkzeug.security import check_password_hash
from app.models.user import User ,Order,Product
from datetime import datetime
from app import db
import hashlib
bp = Blueprint('register', __name__)
# Route to serve the signup page and handle form submission
from werkzeug.security import generate_password_hash

# @bp.route('/', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         # Handle signup form submission here
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         if password != confirm_password:
#             return "Passwords do not match", 400

#         # Hash the password before saving to the database
#         hashed_password = generate_password_hash(password)

#         # Store the user data in the database (make sure to save hashed_password)
#         new_user = User(username=username, email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         return f"Signup successful for {username}!", 201
#         return render_template("login.html")

#     return render_template('index.html')

# from werkzeug.security import check_password_hash
# # Route for login
# @bp.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Fetch the user by email
#         user = User.query.filter_by(email=email).first()

#         if user and check_password_hash(user.password, password):
#             # Correct login, store user info in the session
#             session['user_id'] = user.id
#             session['username'] = user.username
#             flash('Login successful!', 'success')
#             # print(session)
#              # Redirect to dashboard if login is successful
#             # return redirect(url_for('register.dashboard'))
#             return render_template('dashboard.html')
#         else:
#             flash('Invalid username or password', 'danger')  # Show an error message using flash
#             return redirect(url_for('register.login'))  # Redirect back to login page

#     return render_template('login.html')

# @bp.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         flash('Please log in to access the dashboard', 'warning')
#         return redirect(url_for('register.login'))  # Redirect only if not logged in

#     return render_template('dashboard.html', username=session.get('username'))
# @bp.route('/orders')
# def orders():
#     if 'user_id' not in session:
#         flash('Please log in to access orders', 'warning')
#         return redirect(url_for('register.login'))  # Redirect if not logged in

#     user_id = session['user_id']
#     print("Session User ID:", user_id)

#     # ✅ Fetch orders and join with products
#     user_orders = (
#         db.session.query(Order, Product)
#         .join(Product, Order.product_id == Product.id)
#         .filter(Order.user_id == user_id)
#         .all()
#     )

#     print("Fetched Orders:", user_orders)  # Debugging output

#     return render_template('orders.html', orders=user_orders)



# # Route for logout
# @bp.route('/logout')
# def logout():
#     # session.pop('user_id', None)
#     # session.pop('username', None)
#     session.clear()
#     flash('You have been logged out', 'success')
#     return redirect(url_for('register.login'))



# @bp.route('/book', methods=['POST'])
# def book():
#     if 'user_id' not in session:
#         flash("Please log in to book a water can", "warning")
#         return redirect(url_for('register.login'))  # Redirect if user is not logged in

#     user_id = session['user_id']
#     product_id = request.form.get('product_id')
#     quantity = request.form.get('quantity')

#     if not product_id or product_id == "0":
#         flash("Please select a valid product.", "danger")
#         return redirect(url_for('register.dashboard'))

#     if not quantity or int(quantity) < 1:
#         flash("Please enter a valid quantity.", "danger")
#         return redirect(url_for('register.dashboard'))

#     # Check if product exists
#     product = Product.query.get(product_id)
#     if not product:
#         flash("Invalid product selection.", "danger")
#         return redirect(url_for('register.dashboard'))

#     # Create a new order and save to DB
#     new_order = Order(
#         user_id=user_id,
#         product_id=product_id,
#         quantity=int(quantity),
#         order_date=datetime.utcnow()
#     )
#     db.session.add(new_order)
#     db.session.commit()

#     flash("Order placed successfully!", "success")
#     return redirect(url_for('register.orders'))




from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User, Order, Product
from datetime import datetime
from app import db

bp = Blueprint('register', __name__)

@bp.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match", 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('register.login'))

    return render_template('index.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email']=user.email
            flash('Login successful!', 'success')
            return redirect(url_for('register.dashboard'))
            
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('register.login'))

    return render_template('login.html')
@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect('/login')

    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).all()
    products = Product.query.all()

    print(f"📌 Orders for User {user_id}: {orders}")  # Debugging line

    return render_template('dashboard.html', orders=orders, products=products)


@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

@bp.route('/order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return jsonify({'error': 'Missing data'}), 400

    new_order = Order(user_id=session['user_id'], product_id=product_id, quantity=quantity, order_date=datetime.utcnow())
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'})

@bp.route('/orders', methods=['GET'])
def orders():
    user_id = session.get('user_id')
    orders = db.session.query(
        Order.id,
        Order.order_date,
        Product.name.label('product_name'),
        Order.quantity,
        Order.total_price,
        Order.status
    ).join(Product).filter(Order.user_id == user_id).all()

    # Convert SQLAlchemy objects to dictionaries
    order_list = []
    for order in orders:
        order_list.append({
            "id": order.id,
            "order_date": order.order_date.strftime('%Y-%m-%d %H:%M'),
            "product": order.product_name,
            "quantity": order.quantity,
            "total_price": order.total_price,  # ✅ Ensure total_price is included
            "status": order.status
        })

    return render_template("orders.html", orders=order_list)


@bp.route('/book', methods=['POST'])
def book_order():
    try:
        if 'user_id' not in session:
            flash("Please log in first!", "error")
            return redirect('/login')

        user_id = session['user_id']
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')

        print(f"📌 Received Data - User ID: {user_id}, Product ID: {product_id}, Quantity: {quantity}")

        if not product_id or not quantity:
            print("❌ Missing product or quantity!")
            flash("Invalid input!", "error")
            return redirect('/dashboard')

        quantity = int(quantity)
        product = Product.query.get(product_id)

        if not product:
            print("❌ Product not found in DB!")
            flash("Invalid product!", "error")
            return redirect('/dashboard')

        if product.stock < quantity:
            print("❌ Not enough stock available!")
            flash("Not enough stock available!", "error")
            return redirect('/dashboard')

        total_price = product.price * quantity

        # Insert order
        new_order = Order(
            user_id=user_id,
            product_id=product.id,
            quantity=quantity,
            total_price=total_price,
            status='Pending',
            order_date=datetime.utcnow()
        )

        db.session.add(new_order)
        product.stock -= quantity  # Reduce stock
        db.session.commit()

        print("✅ Order stored successfully!")
        # return jsonify({"message": "Order placed successfully!"}), 200
        flash("Order placed successfully!", "success")
        return redirect('/dashboard')

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error during booking: {e}")
        flash("An error occurred while booking. Try again.", "error")
        return redirect('/dashboard')
@bp.route("/home")
def home():
    return render_template("home.html")

@bp.route("/settings")
def settings():
    print("Session Data:", session)  # Debugging step
    return render_template("settings.html", username=session.get("username"), email=session.get("email"))


@bp.route("/update-settings", methods=["POST"])
def update_settings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])
    
    if not user:
        return "User not found", 404

    user.username = request.form.get("username")
    user.email = request.form.get("email")
    user.address=request.form.get("address")

    db.session.commit()  # 🔥 Commit changes

    session["username"] = user.username
    session["email"] = user.email  # Update session data
    session["address"] = user.address

    flash("profile updated successfully!", "success")
    return redirect(url_for("register.settings"))


@bp.route("/logout")
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for("register.login")) 
