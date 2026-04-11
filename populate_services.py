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
            {
                'name': 'Another Language Support',
                'description': 'Personalized support sessions in another language of your choice for study and daily communication.',
                'category': 'Language',
                'subcategory': 'Other Language',
                'price': 45.0,
                'is_available': True
            },
            {
                'name': 'Translation Service',
                'description': 'Formal document and communication translation between English and Italian with clear, accurate wording.',
                'category': 'Language',
                'subcategory': 'Translation',
                'price': 30.0,
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
            },

            # Group Tour Services
            {
                'name': 'Group Tour in Sicily',
                'description': 'Explore Sicily together from just 2 people, with a full package including car rental and a local tour guide.',
                'category': 'Group Tour',
                'subcategory': 'Sicily Tour',
                'price': 65.0,
                'is_available': True
            },

            # Medical Services
            {
                'name': 'Medical Papers Assistance',
                'description': 'Help obtaining medical documents for residence, gym membership, or other purposes',
                'category': 'Medical',
                'subcategory': 'Medical Papers',
                'price': 25.0,
                'is_available': True
            },
            {
                'name': 'Medical Assistance',
                'description': 'Support finding healthcare services, scheduling appointments, and medical guidance',
                'category': 'Medical',
                'subcategory': 'Medical Assistance',
                'price': 30.0,
                'is_available': True
            },

            # Career Services
            {
                'name': 'Internship Application Support',
                'description': 'Guidance on preparing and submitting internship applications. We connect students with internship and job opportunities.',
                'category': 'Career',
                'subcategory': 'Internship',
                'price': 30.0,
                'is_available': True
            },
            {
                'name': 'Job Application Support',
                'description': 'Help with CV tailoring, cover letters, and job application strategy. We connect students with internship and job opportunities.',
                'category': 'Career',
                'subcategory': 'Job Application',
                'price': 35.0,
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
        for category in ['Documentation', 'Housing', 'Language', 'Transportation', 'Group Tour', 'Medical', 'Career']:
            count = Service.query.filter_by(category=category).count()
            print(f"- {category}: {count} services")

if __name__ == '__main__':
    populate_services()
