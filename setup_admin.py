#!/usr/bin/env python3
"""
Setup script to create a clean admin profile
"""

from app import app, db
from models import Admin

def setup_admin():
    with app.app_context():
        # Remove all existing admin users
        Admin.query.delete()
        
        # Create Santiago admin user
        admin = Admin(
            username='Santiago',
            email='santiago@nauticbooking.com'
        )
        admin.set_password('Santiago123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✓ Admin user 'Santiago' created successfully")
        print("✓ Password: Santiago123")
        print("✓ Email: santiago@nauticbooking.com")

if __name__ == "__main__":
    setup_admin()