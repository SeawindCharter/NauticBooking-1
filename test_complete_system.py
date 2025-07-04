#!/usr/bin/env python3
"""
Test completo de TODA la funcionalidad del sistema NauticBooking
"""

import requests
from bs4 import BeautifulSoup
import sys

def test_form_submission(url, form_data, description):
    """Test a form submission and return detailed results"""
    session = requests.Session()
    
    print(f"\n=== TESTING {description.upper()} ===")
    
    # Get the form page
    try:
        response = session.get(url)
        if response.status_code != 200:
            print(f"❌ Cannot access form at {url}")
            return False
        
        # Parse and get CSRF token
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            form_data['csrf_token'] = csrf_input.get('value')
            print(f"✓ CSRF token obtained")
        
        # Submit the form
        submit_response = session.post(url, data=form_data, allow_redirects=False)
        print(f"Submit response: {submit_response.status_code}")
        
        if submit_response.status_code == 302:
            print(f"✓ Form submitted successfully (redirect)")
            redirect_url = submit_response.headers.get('Location')
            print(f"✓ Redirecting to: {redirect_url}")
            return True
        elif submit_response.status_code == 200:
            # Check if there are error messages
            error_soup = BeautifulSoup(submit_response.content, 'html.parser')
            alerts = error_soup.find_all(class_='alert')
            if alerts:
                for alert in alerts:
                    print(f"⚠️ Alert: {alert.get_text().strip()}")
            else:
                print(f"⚠️ Form submitted but no redirect (status 200)")
            return False
        else:
            print(f"❌ Form submission failed: {submit_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing {description}: {str(e)}")
        return False

def test_admin_login():
    """Test admin login specifically"""
    return test_form_submission(
        "http://localhost:5000/admin/login",
        {
            'username': 'Santiago',
            'password': 'Santiago123',
            'remember_me': 'n'
        },
        "Admin Login"
    )

def test_new_reservation():
    """Test creating a new reservation"""
    return test_form_submission(
        "http://localhost:5000/reservation/new",
        {
            'cliente': 'Test Cliente',
            'email_cliente': 'test@example.com',
            'telefono_cliente': '+34 600 000 000',
            'barco': 'Oceanis 51.1',
            'fecha_checkin': '2025-08-01',
            'fecha_checkout': '2025-08-08',
            'hora_inicio': '10:00',
            'hora_finalizacion': '18:00',
            'precio_total': '1500.00',
            'pago_a': '750.00',
            'pago_b': '750.00',
            'apa': '200.00',
            'codigo_promocional': '',
            'extras': '',
            'extras_facturados': '0.00',
            'observaciones': 'Test reservation'
        },
        "New Reservation"
    )

def test_edit_reservation():
    """Test editing Santiago's reservation"""
    return test_form_submission(
        "http://localhost:5000/reservation/2/edit",
        {
            'cliente': 'Santiago EDITADO',
            'email_cliente': 'santiago@nauticbooking.com',
            'telefono_cliente': '+34 600 000 000',
            'barco': 'Oceanis 51.1',
            'fecha_checkin': '2025-08-01',
            'fecha_checkout': '2025-08-08',
            'hora_inicio': '10:00',
            'hora_finalizacion': '18:00',
            'precio_total': '2800.00',
            'pago_a': '1400.00',
            'pago_b': '1400.00',
            'apa': '500.00',
            'codigo_promocional': '',
            'extras': '',
            'extras_facturados': '0.00',
            'observaciones': ''
        },
        "Edit Reservation"
    )

def test_navigation():
    """Test basic navigation"""
    base_url = "http://localhost:5000"
    routes = [
        ("/", "Homepage"),
        ("/reservations", "Reservations"),
        ("/reservation/new", "New Reservation Form"),
        ("/admin/login", "Admin Login"),
        ("/admin/dashboard", "Admin Dashboard")
    ]
    
    print("\n=== TESTING NAVIGATION ===")
    working = 0
    total = len(routes)
    
    for route, name in routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {name}: {route}")
                working += 1
            else:
                print(f"❌ {name}: {route} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {name}: {route} (Error: {str(e)})")
    
    print(f"\nNavigation: {working}/{total} working")
    return working == total

def main():
    print("=== COMPLETE SYSTEM TEST ===")
    
    results = []
    
    # Test navigation first
    results.append(("Navigation", test_navigation()))
    
    # Test admin login
    results.append(("Admin Login", test_admin_login()))
    
    # Test new reservation
    results.append(("New Reservation", test_new_reservation()))
    
    # Test edit reservation
    results.append(("Edit Reservation", test_edit_reservation()))
    
    print("\n=== FINAL RESULTS ===")
    working = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if success:
            working += 1
    
    total = len(results)
    print(f"\nOverall: {working}/{total} tests passing ({(working/total)*100:.1f}%)")
    
    if working == total:
        print("🎉 ALL SYSTEMS WORKING!")
        return True
    else:
        print("⚠️ SYSTEM HAS ISSUES")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)