from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import ServiceRequest

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def index():
    requests = ServiceRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/index.html', requests=requests)

@dashboard.route('/requests')
@login_required
def requests():
    requests = ServiceRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/requests.html', requests=requests)