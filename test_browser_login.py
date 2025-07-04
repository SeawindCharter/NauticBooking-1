#!/usr/bin/env python3
"""
Test browser login functionality to diagnose the frozen screen issue
"""

import requests
from bs4 import BeautifulSoup
import time

def test_browser_login():
    """Test the complete login flow from browser perspective"""
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    print("=== TESTING BROWSER LOGIN FLOW ===")
    
    # Step 1: Get login page
    print("1. Loading login page...")
    response = session.get(f"{base_url}/admin/login")
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print("   ✗ Login page not accessible")
        return False
    
    # Step 2: Parse form and get CSRF token
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_token:
        print("   ✗ CSRF token not found")
        return False
    
    csrf_value = csrf_token.get('value')
    print(f"   ✓ CSRF token: {csrf_value[:20]}...")
    
    # Step 3: Submit login form
    print("2. Submitting login form...")
    login_data = {
        'username': 'Santiago',
        'password': 'Santiago123',
        'csrf_token': csrf_value,
        'remember_me': 'n'
    }
    
    response = session.post(f"{base_url}/admin/login", data=login_data, allow_redirects=False)
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    
    if response.status_code == 302:
        redirect_url = response.headers.get('Location')
        print(f"   ✓ Redirect to: {redirect_url}")
        
        # Step 4: Follow redirect
        print("3. Following redirect...")
        response = session.get(redirect_url if redirect_url.startswith('http') else f"{base_url}{redirect_url}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            if 'Dashboard' in response.text:
                print("   ✓ Dashboard loaded successfully")
                return True
            else:
                print("   ✗ Dashboard not found in response")
                return False
        else:
            print(f"   ✗ Dashboard not accessible: {response.status_code}")
            return False
    else:
        print(f"   ✗ Login failed - no redirect")
        return False

if __name__ == "__main__":
    success = test_browser_login()
    if success:
        print("\n✅ BROWSER LOGIN TEST PASSED")
    else:
        print("\n❌ BROWSER LOGIN TEST FAILED")