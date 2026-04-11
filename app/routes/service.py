from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Service, ServiceRequest, EmployerWorkerRequest
from app.forms import ServiceRequestForm, EmployerWorkerRequestForm

service = Blueprint('service', __name__, url_prefix='/service')


def is_career_service(service_obj):
    return service_obj.category == 'Career' and service_obj.subcategory in ['Internship', 'Job Application']


def is_group_tour_service(service_obj):
    return service_obj.category == 'Group Tour' and service_obj.subcategory == 'Sicily Tour'


def is_other_language_service(service_obj):
    return service_obj.category == 'Language' and service_obj.subcategory == 'Other Language'


def is_translation_service(service_obj):
    return service_obj.category == 'Language' and service_obj.subcategory == 'Translation'


def build_request_notes(notes, tour_cities, preferred_language, translation_from_language, translation_to_language):
    base_notes = (notes or '').strip()
    selected_cities = (tour_cities or '').strip()
    selected_language = (preferred_language or '').strip()
    source_language = (translation_from_language or '').strip()
    target_language = (translation_to_language or '').strip()
    note_lines = []

    if selected_cities:
        note_lines.append(f"Preferred tour cities: {selected_cities}")

    if selected_language:
        note_lines.append(f"Selected language: {selected_language}")

    if source_language and target_language:
        note_lines.append(f"Translation: {source_language} to {target_language}")

    if base_notes:
        note_lines.append(base_notes)

    if not note_lines:
        return None
    return "\n".join(note_lines)

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
        selected_service = Service.query.get(form.service_id.data)
        if selected_service is None:
            flash('Selected service is not available.')
            return redirect(url_for('service.request_service'))

        if is_career_service(selected_service):
            required_fields = [
                ('degree_level', form.degree_level.data),
                ('past_degree', form.past_degree.data),
                ('italian_language_level', form.italian_language_level.data)
            ]
            missing = [label for label, value in required_fields if not value or not str(value).strip()]
            if missing:
                flash('Degree level, past degree, and Italian language level are required for Internship and Job Application requests. Experience is optional.')
                return render_template('service/request.html', form=form, services=services, is_career_service=False)

        if is_group_tour_service(selected_service) and not (form.tour_cities.data or '').strip():
            flash('Please enter at least one city in Sicily for your group tour.')
            return render_template('service/request.html', form=form, services=services, is_career_service=False)

        if is_other_language_service(selected_service) and not (form.preferred_language.data or '').strip():
            flash('Please choose your preferred language for this language support request.')
            return render_template('service/request.html', form=form, services=services, is_career_service=False)

        if is_translation_service(selected_service):
            source_language = (form.translation_from_language.data or '').strip()
            target_language = (form.translation_to_language.data or '').strip()
            if not source_language or not target_language:
                flash('Please choose both source and target language for translation.')
                return render_template('service/request.html', form=form, services=services, is_career_service=False)
            if source_language == target_language:
                flash('Source and target language must be different for translation.')
                return render_template('service/request.html', form=form, services=services, is_career_service=False)

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
            requester_full_name=current_user.full_name or current_user.email,
            notes=build_request_notes(
                form.notes.data,
                form.tour_cities.data,
                form.preferred_language.data,
                form.translation_from_language.data,
                form.translation_to_language.data
            ),
            degree_level=form.degree_level.data,
            past_degree=form.past_degree.data,
            experience=form.experience.data,
            italian_language_level=form.italian_language_level.data,
            languages=form.languages.data
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('dashboard.requests'))
    
    return render_template('service/request.html', form=form, services=services, is_career_service=False)

@service.route('/<int:id>/request', methods=['GET', 'POST'])
@login_required 
def request_specific_service(id):
    service = Service.query.get_or_404(id)
    form = ServiceRequestForm()
    
    # Pre-select the service
    form.service_id.choices = [(service.id, f"{service.category} - {service.name}")]
    form.service_id.data = service.id
    
    if form.validate_on_submit():
        if is_career_service(service):
            required_fields = [
                ('degree_level', form.degree_level.data),
                ('past_degree', form.past_degree.data),
                ('italian_language_level', form.italian_language_level.data)
            ]
            missing = [label for label, value in required_fields if not value or not str(value).strip()]
            if missing:
                flash('Degree level, past degree, and Italian language level are required for Internship and Job Application requests. Experience is optional.')
                return render_template('service/request.html', form=form, service=service, is_career_service=is_career_service(service))

        if is_group_tour_service(service) and not (form.tour_cities.data or '').strip():
            flash('Please enter at least one city in Sicily for your group tour.')
            return render_template('service/request.html', form=form, service=service, is_career_service=is_career_service(service))

        if is_other_language_service(service) and not (form.preferred_language.data or '').strip():
            flash('Please choose your preferred language for this language support request.')
            return render_template('service/request.html', form=form, service=service, is_career_service=is_career_service(service))

        if is_translation_service(service):
            source_language = (form.translation_from_language.data or '').strip()
            target_language = (form.translation_to_language.data or '').strip()
            if not source_language or not target_language:
                flash('Please choose both source and target language for translation.')
                return render_template('service/request.html', form=form, service=service, is_career_service=is_career_service(service))
            if source_language == target_language:
                flash('Source and target language must be different for translation.')
                return render_template('service/request.html', form=form, service=service, is_career_service=is_career_service(service))

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
            requester_full_name=current_user.full_name or current_user.email,
            notes=build_request_notes(
                form.notes.data,
                form.tour_cities.data,
                form.preferred_language.data,
                form.translation_from_language.data,
                form.translation_to_language.data
            ),
            degree_level=form.degree_level.data,
            past_degree=form.past_degree.data,
            experience=form.experience.data,
            italian_language_level=form.italian_language_level.data,
            languages=form.languages.data
        )
        db.session.add(service_request)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('dashboard.requests'))
    
    return render_template('service/request.html', form=form, service=service, is_career_service=is_career_service(service))


@service.route('/employer-request', methods=['GET', 'POST'])
def employer_request():
    form = EmployerWorkerRequestForm()

    if form.validate_on_submit():
        employer_request_obj = EmployerWorkerRequest(
            employer_name=form.employer_name.data,
            work_category=form.work_category.data,
            work_type=form.work_type.data,
            short_term_days=form.short_term_days.data if form.work_type.data == 'short_term' else None,
            preferred_start_date=form.preferred_start_date.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            details=form.details.data,
        )
        db.session.add(employer_request_obj)
        db.session.commit()
        flash('Your worker request has been submitted successfully. Our team will contact you soon.')
        return redirect(url_for('service.employer_request'))

    return render_template('service/employer_request.html', form=form)