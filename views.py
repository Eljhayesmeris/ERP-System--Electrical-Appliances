from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import SellerInfo, BuyerInfo, User
from . import db
import json
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI mode
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_caching import Cache
from . import app


views = Blueprint('views', __name__)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  

@cache.cached(timeout=300, key_prefix='/')
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Query the database to get the counts
    num_buyers = BuyerInfo.query.count()
    num_sellers = SellerInfo.query.count()
    total_users = User.query.count()

    chart_base64 = generate_bar_chart(num_buyers, num_sellers, total_users)

    return render_template("home.html", user=current_user, num_buyers=num_buyers, num_sellers=num_sellers, chart_base64=chart_base64, total_users=total_users)


def generate_bar_chart(num_buyers, num_sellers, total_users):
    # Data
    categories = ['Buyers', 'Sellers', 'Total Users']
    data = [num_buyers, num_sellers, total_users]

    # Create the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(categories, data, color=['blue', 'green', 'red'])
    plt.xlabel('User Type')
    plt.ylabel('Number of Accounts')
    plt.title('User Accounts Summary')
    plt.tight_layout()

    # Convert the chart to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_base64 = base64.b64encode(buffer.read()).decode()
    buffer.close()

    return chart_base64
