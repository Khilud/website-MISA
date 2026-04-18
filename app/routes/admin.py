from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Service, ServiceRequest, EmployerWorkerRequest
from app.forms import ServiceForm, UpdateRequestForm, UpdateEmployerRequestStatusForm, DeleteUserForm
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
            category=form.category.data,
            subcategory=form.subcategory.data if form.subcategory.data else None,
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
        service.category = form.category.data
        service.subcategory = form.subcategory.data if form.subcategory.data else None
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
    selected_status = (request.args.get('status') or '').strip().lower()

    requests_query = ServiceRequest.query.order_by(ServiceRequest.request_date.desc())
    employer_requests_query = EmployerWorkerRequest.query.order_by(EmployerWorkerRequest.request_date.desc())

    if selected_status == 'pending':
        requests_query = requests_query.filter(ServiceRequest.status == 'pending')
        employer_requests_query = employer_requests_query.filter(EmployerWorkerRequest.status == 'pending')

    requests = requests_query.all()
    grouped_requests = {
        'documentation': [],
        'language': [],
        'housing': [],
        'career': [],
        'tour': [],
        'other': [],
    }

    for service_request in requests:
        grouped_requests.setdefault(service_request.request_type_key, []).append(service_request)

    request_sections = [
        {'key': 'documentation', 'label': 'Documentation', 'requests': grouped_requests['documentation']},
        {'key': 'language', 'label': 'Language', 'requests': grouped_requests['language']},
        {'key': 'housing', 'label': 'Housing', 'requests': grouped_requests['housing']},
        {'key': 'career', 'label': 'Career', 'requests': grouped_requests['career']},
        {'key': 'tour', 'label': 'Tour', 'requests': grouped_requests['tour']},
    ]
    other_requests = grouped_requests['other']
    employer_requests = employer_requests_query.all()
    return render_template(
        'admin/requests.html',
        requests=requests,
        request_sections=request_sections,
        other_requests=other_requests,
        employer_requests=employer_requests,
        selected_status=selected_status,
    )


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.is_admin.desc(), User.full_name.asc()).all()
    delete_form = DeleteUserForm()
    return render_template('admin/users.html', users=users, delete_form=delete_form)


@admin.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    form = DeleteUserForm()
    if not form.validate_on_submit():
        flash('Invalid delete request.')
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.')
        return redirect(url_for('admin.users'))

    ServiceRequest.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('admin.users'))

@admin.route('/requests/<int:id>/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_request(id):
    service_request = ServiceRequest.query.get_or_404(id)
    form = UpdateRequestForm()
    if form.validate_on_submit():
        service_request.status = form.status.data
        service_request.notes = form.notes.data
        if form.status.data == 'completed':
            service_request.completion_date = datetime.utcnow()
        db.session.commit()
        flash('Request updated successfully!')
        return redirect(url_for('admin.requests'))
    elif request.method == 'GET':
        form.status.data = service_request.status
        form.notes.data = service_request.notes
    return render_template('admin/update_request.html', form=form, service_request=service_request)


@admin.route('/employer-requests/<int:id>/update', methods=['GET', 'POST'])
@login_required
@admin_required
def update_employer_request(id):
    employer_request = EmployerWorkerRequest.query.get_or_404(id)
    form = UpdateEmployerRequestStatusForm()
    if form.validate_on_submit():
        employer_request.status = form.status.data
        db.session.commit()
        flash('Employer request updated successfully!')
        return redirect(url_for('admin.requests'))
    elif request.method == 'GET':
        form.status.data = employer_request.status
    return render_template('admin/update_employer_request.html', form=form, employer_request=employer_request)