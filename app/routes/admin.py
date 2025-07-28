from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Service, ServiceRequest
from app.forms import ServiceForm, UpdateRequestForm
from datetime import datetime
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def index():
    users_count = User.query.count()
    services_count = Service.query.count()
    requests_count = ServiceRequest.query.count()
    pending_requests = ServiceRequest.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                          users_count=users_count,
                          services_count=services_count,
                          requests_count=requests_count,
                          pending_requests=pending_requests)

@admin.route('/services')
@login_required
@admin_required
def services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)

@admin.route('/services/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            is_available=form.is_available.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully!')
        return redirect(url_for('admin.services'))
    return render_template('admin/add_service.html', form=form)

@admin.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.is_available = form.is_available.data
        db.session.commit()
        flash('Service updated successfully!')
        return redirect(url_for('admin.services'))
    return render_template('admin/edit_service.html', form=form, service=service)

@admin.route('/requests')
@login_required
@admin_required
def requests():
    requests = ServiceRequest.query.all()
    return render_template('admin/requests.html', requests=requests)

@admin.route('/requests/<int:id>/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_request(id):
    service_request = ServiceRequest.query.get_or_404(id)
    form = UpdateRequestForm(obj=service_request)
    if form.validate_on_submit():
        service_request.status = form.status.data
        service_request.notes = form.notes.data
        if form.status.data == 'completed':
            service_request.completion_date = datetime.utcnow()
        db.session.commit()
        flash('Request updated successfully!')
        return redirect(url_for('admin.requests'))
    return render_template('admin/update_request.html', form=form, service_request=service_request)