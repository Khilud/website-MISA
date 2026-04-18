from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import ServiceRequest
from app.forms import ProfileUpdateForm

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def index():
    requests = ServiceRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/index.html', requests=requests)


@dashboard.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm(original_email=current_user.email)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data.strip()
        current_user.gender = form.gender.data or None
        current_user.department = form.department.data
        current_user.phone_number = form.phone_number.data
        current_user.email = form.email.data.strip()
        db.session.commit()
        flash('Your profile has been updated successfully.')
        return redirect(url_for('dashboard.index'))

    if request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.gender.data = current_user.gender or ''
        form.department.data = current_user.department
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email

    requests = ServiceRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/profile.html', form=form, requests=requests)

@dashboard.route('/requests')
@login_required
def requests():
    requests = ServiceRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/requests.html', requests=requests)