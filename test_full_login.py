#!/usr/bin/env python3
"""
Test complete login flow to diagnose and fix the issue
"""

import requests
from bs4 import BeautifulSoup

def test_complete_login():
    session = requests.Session()
    
    print("=== TESTING COMPLETE LOGIN FLOW ===")
    
    # Step 1: Get login page and extract CSRF token
    print("1. Getting login page...")
    login_page = session.get('http://localhost:5000/admin/login')
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    print(f"   CSRF token: {csrf_token[:20]}...")
    
    # Step 2: Submit login form
    print("2. Submitting login form...")
    login_data = {
        'username': 'Santiago',
        'password': 'Santiago123',
        'csrf_token': csrf_token
    }
    
    login_response = session.post('http://localhost:5000/admin/login', data=login_data, allow_redirects=False)
    print(f"   Login response status: {login_response.status_code}")
    print(f"   Location header: {login_response.headers.get('Location', 'None')}")
    
    # Step 3: Follow redirect if exists
    if login_response.status_code in [301, 302]:
        print("3. Following redirect...")
        redirect_url = login_response.headers.get('Location')
        if redirect_url.startswith('/'):
            redirect_url = 'http://localhost:5000' + redirect_url
        
        dashboard_response = session.get(redirect_url)
        print(f"   Dashboard response status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            if 'Dashboard' in dashboard_response.text:
                print("   ✓ Login successful - reached dashboard")
            else:
                print("   ✗ Reached page but not dashboard")
        else:
            print(f"   ✗ Dashboard failed with status {dashboard_response.status_code}")
    else:
        print("   ✗ No redirect after login")
        if 'Error' in login_response.text:
            print("   Login form showing error")

if __name__ == "__main__":
    test_complete_login()