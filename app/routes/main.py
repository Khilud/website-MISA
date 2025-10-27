from flask import Blueprint, render_template, jsonify , request
from flask_login import current_user , login_required
from app.models import Service , ServiceRequest
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get limited services for featured section - 2 from each category
    featured_services = {}
    categories = ['Documentation', 'Housing', 'Language', 'Transportation']
    
    for category in categories:
        services = Service.query.filter_by(category=category, is_available=True).limit(2).all()
        if services:
            featured_services[category] = services
    
    return render_template('home.html', featured_services=featured_services)

@main.route('/services')
def services():
    user_services = []
    if current_user.is_authenticated:
        user_services = [s.service_id for s in ServiceRequest.query.filter_by(user_id=current_user.id).all()]
    
    # Get services grouped by category
    services_by_category = {}
    all_services = Service.query.filter_by(is_available=True).all()
    
    for service in all_services:
        if service.category not in services_by_category:
            services_by_category[service.category] = []
        services_by_category[service.category].append(service)
    
    return render_template('service/details.html',
                         services_by_category=services_by_category,
                         user_services=user_services)

@main.route('/add-service', methods=['POST'])
@login_required
def add_service():
    try:
        data = request.get_json()
        service_id = data.get('service_id')
        
        # Check if service exists and is available
        service = Service.query.filter_by(id=service_id, is_available=True).first()
        if not service:
            return jsonify({'success': False, 'error': 'Service not found or unavailable'}), 400
        
        # Check if user already has a pending request for this service
        existing_request = ServiceRequest.query.filter_by(
            user_id=current_user.id,
            service_id=service_id,
            status='pending'
        ).first()
        
        if existing_request:
            return jsonify({'success': False, 'error': 'You already have a pending request for this service'}), 400
        
        new_request = ServiceRequest(
            user_id=current_user.id,
            service_id=service_id,
            status='pending'
        )
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Service request submitted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@main.route('/remove-service', methods=['POST'])
@login_required
def remove_service():
    try:
        data = request.get_json()
        service_id = data.get('service_id')
        
        service_request = ServiceRequest.query.filter_by(
            user_id=current_user.id,
            service_id=service_id
        ).first()
        
        if service_request:
            db.session.delete(service_request)
            db.session.commit()
            
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/future-plans')
def future_plans():
    return render_template('future_plans.html')