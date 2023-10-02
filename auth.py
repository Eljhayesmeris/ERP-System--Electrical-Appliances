from sqlite3 import IntegrityError
import traceback
from flask import Blueprint, Flask, render_template, request, flash, redirect, url_for
from .models import User, BuyerInfo, SellerInfo
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import random
from .models import CartItem, Products
import string
from flask_bcrypt import Bcrypt
from flask_caching import Cache


auth = Blueprint('auth', __name__)

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  

# Define the login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        # Try to find the user by email
        user = User.query.filter_by(email=username_or_email).first()

        # If the user was not found by email, try to find by username
        if not user:
            user = User.query.filter_by(username=username_or_email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            if user.role == 'admin':
                flash('Logged in as admin!', category='success')
                return render_template("home.html", user=current_user)
            elif user.role == 'buyer':
                flash('Logged in as a buyer!', category='success')
                return render_template("buyer.html", user=current_user)
            elif user.role == 'seller':
                flash('Logged in as a seller!', category='success')
                return render_template("seller.html", user=current_user)
        else:
            flash('Incorrect username or password. Please try again.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/buyer_registration', methods=['GET', 'POST'])
def buyer_registration():
    if request.method == 'POST':
        # Get user registration data from the form
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Additional fields for buyer
        full_name = request.form.get('full-name')
        contact_number = request.form.get('contact-number')
        buyer_address = request.form.get('buyer-address')  # Note the field name

        # Check if passwords match and other validation
        if password1 != password2:
            flash('Passwords don\'t match. Please try again.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        elif not email:
            flash("Email must be provided.", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')

            # Create a new user record in the User table
            new_user = User(username=username, email=email, password=hashed_password, role='buyer')  # Set the role to 'buyer'
            db.session.add(new_user)
            db.session.commit()

            # Create a record in BuyerInfo
            buyer_info = BuyerInfo(
                full_name=full_name,
                contact_number=contact_number,
                address=buyer_address,
                user_id=new_user.id
            )
            db.session.add(buyer_info)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))

    return render_template("buyer_registration.html", user=current_user)

@auth.route('/seller_registration', methods=['GET', 'POST'])
def seller_registration():
    if request.method == 'POST':
        # Get user registration data from the form
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Additional fields for seller
        full_name = request.form.get('full-name')
        contact_number = request.form.get('contact-number')
        address = request.form.get('address')  # Note the field name
        shop_name = request.form.get('shop-name')
        description = request.form.get('shop-description')
        shop_address = request.form.get('shop-Address')

        # Check if passwords match and other validation
        if password1 != password2:
            flash('Passwords don\'t match. Please try again.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        elif not email:
            flash("Email must be provided.", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')

            # Create a new user record in the User table
            new_user = User(username=username, email=email, password=hashed_password, role='seller')  # Set the role to 'seller'
            db.session.add(new_user)
            db.session.commit()

            # Create a record in SellerInfo
            seller_info = SellerInfo(
                full_name=full_name,
                contact_number=contact_number,
                address=address,
                shop_name=shop_name,
                description=description,
                shop_address=shop_address,
                user_id=new_user.id
            )
            db.session.add(seller_info)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created successfully!', 'success')
            return redirect(url_for('auth.login'))

    return render_template("seller_registration.html", user=current_user)


@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))



products = [
    {'id': 1, 'name': 'Product 1', 'category': 'Appliances', 'price': 100},
    {'id': 2, 'name': 'Product 2', 'category': 'Electronics', 'price': 200},
    {'id': 3, 'name': 'Product 3', 'category': 'Appliances', 'price': 150},
    {'id': 4, 'name': 'Product 4', 'category': 'Electronics', 'price': 250},
]

@auth.route('/products')
def filtered_products():
    category = request.args.get('category')
    
    # Implement product filtering based on the selected category
    if category:
        filtered = [product for product in products if product['category'] == category]
    else:
        filtered = products  # If no category selected, show all products
    
    return render_template('products.html', products=filtered, user=current_user)


@auth.route('/cart.html', methods=['GET', 'POST'])
@login_required
def cart():
   

    return render_template("cart.html", user=current_user)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    user = None  # You need to define the 'user' variable here based on your application logic

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a temporary password
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Update the user's password to the temporary password
            user.password = temp_password
            db.session.commit()

            # Send an email with the temporary password to the user
            # You'll need to implement email sending here
            # Example using Flask-Mail:
            # from flask_mail import Message
            # from yourapp.extensions import mail
            # msg = Message('Password Reset', sender='your@example.com', recipients=[user.email])
            # msg.body = f'Your temporary password is: {temp_password}'
            # mail.send(msg)

            flash('An email with instructions to reset your password has been sent to your email address.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Email address not found.', 'error')

    return render_template('forgot_password.html',  user=user)


@auth.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Get form data
        name = request.form['productName']
        description = request.form['productDescription']
        price = float(request.form['productPrice'])
        # You can also get other fields like 'productQuantity', 'productImage', and 'category'

        # Create a new Product object
        new_product = Products(
            name=name,
            description=description,
            price=price,
            category='your_category_here'  # Replace with the actual category
        )

        # Add the product to the database session and commit
        db.session.add(new_product)
        db.session.commit()

        # Redirect to a success page or product listing
        return redirect(url_for('product_list'))
    

@auth.route('/terms/seller')
def seller_terms():
    # Render the terms and conditions page for sellers
    return render_template('terms.html')

@auth.route('/terms/buyer')
def buyer_terms():
    # Render the terms and conditions page for buyers
    return render_template('terms.html')    


@auth.route('/terms')
def terms():
    # Render the terms and conditions page
    return render_template('terms.html')


# Function to get buyer data
def get_buyers():
    buyers = BuyerInfo.query.all()  # Retrieve all buyer records
    return buyers

# Function to get seller data
def get_sellers():
    sellers = SellerInfo.query.all()  # Retrieve all seller records
    return sellers

@auth.route('/buyer_accounts.html')
def buyer_accounts():
    buyers = get_buyers()  # Retrieve buyer account data

    return render_template('buyer_accounts.html', buyers=buyers, user=current_user)



@auth.route('/seller_accounts.html')
def seller_accounts():
    sellers = get_sellers()  # Retrieve buyer account data

    return render_template('seller_accounts.html', sellers=sellers, user=current_user)

# Route for buyer.html 
@auth.route('/buyer')
def buyer():
    return render_template('buyer.html', user=current_user)

#Route for seller.html
@auth.route('/seller')
def seller():
    return render_template('seller.html', user=current_user)

# Route for sellertransactions.html 
@auth.route('/transactions')
def transactions():
    return render_template('transactions.html', user=current_user)

# Route for admintrans.html 
@cache.cached(timeout=300, key_prefix='admintrans')
@auth.route('/admintrans')
def admintrans():
    return render_template('admintrans.html', user=current_user)

# Route for buyertrans.html 
@auth.route('/buyertrans')
def buyertrans():
    return render_template('buyertrans.html', user=current_user)

@auth.route('/addtocart')
def addtocart():
    return render_template('addtocart.html', user=current_user)

@auth.route('/payout-request')
def payout_request():
    return render_template('payout-request.html', user=current_user)

@auth.route('/request-payout')
def request_payout():
    return render_template('request-payout.html', user=current_user)

@auth.route('/my_account', methods=['GET', 'POST'])
@login_required
def my_account():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        # Update the username if it has changed
        if new_username != current_user.username:
            current_user.username = new_username
            db.session.commit()
            flash('Username updated successfully.', 'success')

        # Update the password if a new one is provided
        if new_password:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully.', 'success')

        return redirect(url_for('my_account'))

    return render_template('my_account.html')

