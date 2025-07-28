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

@service.route('/<int:id>/request', methods=['GET', 'POST'])
@login_required
def request_service(id):
    service = Service.query.get_or_404(id)
    form = ServiceRequestForm()
    
    if form.validate_on_submit():
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