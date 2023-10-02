from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    role = db.Column(db.String(64), nullable=False, default='buyer')  # Add this line for the 'role' attribute

    # Define relationships with the buyer and seller tables
    buyer_info = db.relationship('BuyerInfo', backref='user', uselist=False)
    seller_info = db.relationship('SellerInfo', backref='user', uselist=False)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)


class BuyerInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

class SellerInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(200))  # Changed field name to 'seller_address'
    shop_name = db.Column(db.String(150))
    description = db.Column(db.String(500))
    shop_address = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)



class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=False)

class CartItem(db.Model):
    # Define the CartItem model with the relationship to Product
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Products', backref='cart_items')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', name='fk_cartitem_product_id'), nullable=False)
