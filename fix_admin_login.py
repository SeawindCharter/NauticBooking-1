#!/usr/bin/env python3
"""
Fix admin login issue - ensure Santiago login works
"""

from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def fix_admin_login():
    with app.app_context():
        # Remove ALL admin users first
        Admin.query.delete()
        db.session.commit()
        
        # Create Santiago with correct password
        admin = Admin()
        admin.username = 'Santiago'
        admin.email = 'santiago@nauticbooking.com'
        admin.password_hash = generate_password_hash('Santiago123')
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"✓ Admin user created: Santiago")
        print(f"✓ Password: Santiago123")
        print(f"✓ Password hash: {admin.password_hash[:50]}...")
        
        # Test the login
        test_admin = Admin.query.filter_by(username='Santiago').first()
        if test_admin and test_admin.check_password('Santiago123'):
            print("✓ Login test: SUCCESS")
        else:
            print("✗ Login test: FAILED")

if __name__ == "__main__":
    fix_admin_login()