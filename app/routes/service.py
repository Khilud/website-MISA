from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Service, ServiceRequest
from app.forms import ServiceRequestForm

service = Blueprint('service', __name__, url_prefix='/service')

@service.route('/')
def index():
    services = Service.query.filter_by(is_available=True).all()
    return render_template('service/index.html', services=services)

@service.route('/<int:id>')
def details(id):
    service = Service.query.get_or_404(id)
    return render_template('service/details.html', service=service)

@service.route('/request', methods=['GET', 'POST'])
@login_required
def request_service():
    form = ServiceRequestForm()
    
    # Populate the service choices
    services = Service.query.filter_by(is_available=True).all()
    form.service_id.choices = [(s.id, f"{s.category} - {s.name}") for s in services]
    
    if form.validate_on_submit():
        # Check if user already has a pending request for this service
        existing_request = ServiceRequest.query.filter_by(
            user_id=current_user.id,
            service_id=form.service_id.data,
            status='pending'
        ).first()
        
        if existing_request:
            flash('You already have a pending request for this service.')
            return redirect(url_for('service.request_service'))
        
        service_request = ServiceRequest(
            user_id=current_user.id,
            service_id=form.service_id.data,
            notes=form.notes.data
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('dashboard.requests'))
    
    return render_template('service/request.html', form=form, services=services)

@service.route('/<int:id>/request', methods=['GET', 'POST'])
@login_required 
def request_specific_service(id):
    service = Service.query.get_or_404(id)
    form = ServiceRequestForm()
    
    # Pre-select the service
    form.service_id.choices = [(service.id, f"{service.category} - {service.name}")]
    form.service_id.data = service.id
    
    if form.validate_on_submit():
        # Check if user already has a pending request for this service
        existing_request = ServiceRequest.query.filter_by(
            user_id=current_user.id,
            service_id=service.id,
            status='pending'
        ).first()
        
        if existing_request:
            flash('You already have a pending request for this service.')
            return redirect(url_for('service.details', id=service.id))
        
        service_request = ServiceRequest(
            user_id=current_user.id,
            service_id=service.id,
            notes=form.notes.data
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('dashboard.requests'))
    
    return render_template('service/request.html', form=form, service=service)