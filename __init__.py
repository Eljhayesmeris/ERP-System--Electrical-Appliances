from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache



  
app = Flask(__name__)
bcrypt = Bcrypt(app)
    
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)    

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdsadsaf'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    
    db.init_app(app)
    # Create a database connection pool
    db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_size=20, max_overflow=0)
    migrate = Migrate(app, db)
    
    from .views import views
    from .auth import auth 
    from .models import User, Products, CartItem, BuyerInfo, SellerInfo # Import your models here
 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    # Create the database tables for your models
    with app.app_context():
        db.create_all()
        

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


