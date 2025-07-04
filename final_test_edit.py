#!/usr/bin/env python3
"""
Final test to demonstrate complete edit workflow
"""

import requests
from bs4 import BeautifulSoup
import sys

def final_test():
    """Test the complete edit workflow"""
    base_url = "http://localhost:5000"
    
    print("=== FINAL COMPLETE TEST ===")
    
    # Step 1: Check current state
    print("\n1. Checking current Santiago reservation...")
    with requests.Session() as session:
        # Get current state
        reservations_page = session.get(f"{base_url}/reservations")
        if reservations_page.status_code != 200:
            print(f"❌ Cannot access reservations page: {reservations_page.status_code}")
            return False
        
        soup = BeautifulSoup(reservations_page.content, 'html.parser')
        santiago_row = None
        for row in soup.find_all('tr'):
            if 'Santiago' in str(row):
                santiago_row = row
                break
        
        if not santiago_row:
            print("❌ Santiago reservation not found")
            return False
        
        print("✓ Santiago reservation found")
        
        # Step 2: Get edit page
        print("\n2. Accessing edit page...")
        edit_page = session.get(f"{base_url}/reservation/2/edit")
        if edit_page.status_code != 200:
            print(f"❌ Cannot access edit page: {edit_page.status_code}")
            return False
        
        print("✓ Edit page accessible")
        
        # Step 3: Submit edit form
        print("\n3. Submitting edit form...")
        edit_soup = BeautifulSoup(edit_page.content, 'html.parser')
        csrf_token = edit_soup.find('input', {'name': 'csrf_token'})
        if not csrf_token:
            print("❌ CSRF token not found")
            return False
        
        form_data = {
            'csrf_token': csrf_token['value'],
            'cliente': 'Santiago FINAL TEST',
            'email_cliente': 'santiago@test.com',
            'telefono_cliente': '+34 600 000 000',
            'barco': 'Oceanis 51.1',
            'fecha_checkin': '2025-08-01',
            'fecha_checkout': '2025-08-08',
            'hora_inicio': '10:00',
            'hora_finalizacion': '18:00',
            'precio_total': '3000.00',
            'pago_a': '1500.00',
            'pago_b': '1500.00',
            'apa': '300.00',
            'codigo_promocional': '',
            'extras': 'Final test edit',
            'extras_facturados': '0.00',
            'observaciones': 'Final test observation'
        }
        
        edit_response = session.post(f"{base_url}/reservation/2/edit", data=form_data, allow_redirects=False)
        
        print(f"Edit response status: {edit_response.status_code}")
        if edit_response.status_code == 302:
            print("✓ Form submitted successfully (redirect)")
            redirect_url = edit_response.headers.get('Location', '')
            print(f"✓ Redirect to: {redirect_url}")
        else:
            print(f"❌ Form submission failed: {edit_response.status_code}")
            return False
        
        # Step 4: Verify the change
        print("\n4. Verifying changes...")
        verify_page = session.get(f"{base_url}/reservations")
        verify_soup = BeautifulSoup(verify_page.content, 'html.parser')
        
        found_final_test = False
        for row in verify_soup.find_all('tr'):
            if 'Santiago FINAL TEST' in str(row):
                found_final_test = True
                print("✓ Change confirmed: 'Santiago FINAL TEST' found in reservations")
                break
        
        if not found_final_test:
            print("❌ Change not found in reservations list")
            # Check what's actually there
            for row in verify_soup.find_all('tr'):
                if 'Santiago' in str(row):
                    print(f"Found Santiago row: {row.get_text()}")
            return False
        
        print("\n🎉 ALL TESTS PASSED - EDIT FUNCTIONALITY WORKING!")
        return True

if __name__ == "__main__":
    success = final_test()
    sys.exit(0 if success else 1)