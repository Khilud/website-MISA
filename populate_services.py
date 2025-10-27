#!/usr/bin/env python3
"""
Script to populate the database with predefined services
Run this after creating the database schema
"""

from app import create_app, db
from app.models import Service

def populate_services():
    app = create_app()
    
    with app.app_context():
        # Clear existing services if any
        Service.query.delete()
        
        # Define predefined services
        services_data = [
            # Documentation Services
            {
                'name': 'Document Appointments',
                'description': 'Assistance with booking appointments for various official documents',
                'category': 'Documentation',
                'subcategory': 'Appointments',
                'price': 15.0,
                'is_available': True
            },
            {
                'name': 'ISEE Application',
                'description': 'Help with ISEE (Equivalent Economic Status Indicator) application process',
                'category': 'Documentation',
                'subcategory': 'ISEE',
                'price': 25.0,
                'is_available': True
            },
            {
                'name': 'Residence Permit',
                'description': 'Assistance with residence permit application and renewal',
                'category': 'Documentation',
                'subcategory': 'Residence Permit',
                'price': 30.0,
                'is_available': True
            },
            {
                'name': 'University Enrollment',
                'description': 'Support with university enrollment processes and documentation',
                'category': 'Documentation',
                'subcategory': 'Enrollment',
                'price': 20.0,
                'is_available': True
            },
            
            # Housing Services
            {
                'name': 'Permanent Housing',
                'description': 'Assistance finding permanent accommodation solutions',
                'category': 'Housing',
                'subcategory': 'Permanent',
                'price': 50.0,
                'is_available': True
            },
            {
                'name': 'Temporary Housing',
                'description': 'Short-term accommodation assistance for new arrivals',
                'category': 'Housing',
                'subcategory': 'Temporary',
                'price': 35.0,
                'is_available': True
            },
            
            # Language Services
            {
                'name': 'Italian Language Lessons',
                'description': 'Italian language classes for international students',
                'category': 'Language',
                'subcategory': 'Italian Lessons',
                'price': 40.0,
                'is_available': True
            },
            {
                'name': 'English Language Support',
                'description': 'English language tutoring and conversation practice',
                'category': 'Language',
                'subcategory': 'English Lessons',
                'price': 35.0,
                'is_available': True
            },
            
            # Transportation Services
            {
                'name': 'Airport Pickup Service',
                'description': 'Transportation from airport to accommodation for new arrivals',
                'category': 'Transportation',
                'subcategory': 'Airport Pickup',
                'price': 45.0,
                'is_available': True
            }
        ]
        
        # Add services to database
        for service_data in services_data:
            service = Service(**service_data)
            db.session.add(service)
        
        db.session.commit()
        print(f"Successfully added {len(services_data)} services to the database!")
        
        # Print summary
        for category in ['Documentation', 'Housing', 'Language', 'Transportation']:
            count = Service.query.filter_by(category=category).count()
            print(f"- {category}: {count} services")

if __name__ == '__main__':
    populate_services()
