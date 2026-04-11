#!/usr/bin/env python3
"""
Script to reset admin password
"""

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def reset_admin_password():
    app = create_app()
    
    with app.app_context():
        # Find the admin user
        admin_user = User.query.filter_by(is_admin=True).first()
        
        if admin_user:
            # Set new password
            new_password = "admin123"
            admin_user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            
            print(f"Admin password reset successfully!")
            print(f"Name: {admin_user.display_name}")
            print(f"Email: {admin_user.email}")
            print(f"New Password: {new_password}")
            print("\nYou can now login with these credentials.")
        else:
            print("No admin user found in database!")

if __name__ == '__main__':
    reset_admin_password()
