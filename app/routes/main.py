from flask import Blueprint, render_template
from flask_login import current_user
from app.models import Service

main = Blueprint('main', __name__)

@main.route('/')
def index():
    services = Service.query.filter_by(is_available=True).all()
    return render_template('home.html', services=services)