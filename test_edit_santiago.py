#!/usr/bin/env python3
"""
Test específico para editar la reserva de Santiago y verificar que se guarda correctamente
"""

import requests
from bs4 import BeautifulSoup
import sys

def test_santiago_edit():
    """Test editing Santiago's reservation"""
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    print("=== TESTING SANTIAGO RESERVATION EDIT ===")
    
    # Step 1: Find Santiago's reservation ID
    print("1. Finding Santiago's reservation...")
    reservations_response = session.get(f"{base_url}/reservations")
    
    if reservations_response.status_code != 200:
        print("❌ Cannot access reservations page")
        return False
    
    soup = BeautifulSoup(reservations_response.content, 'html.parser')
    santiago_row = None
    reservation_id = None
    
    # Look for Santiago in the table
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if cells and len(cells) > 0:
            if 'Santiago' in cells[0].get_text():
                # Extract reservation ID from the edit link
                edit_link = row.find('a', href=lambda x: x and 'edit' in x)
                if edit_link:
                    href = edit_link.get('href')
                    reservation_id = href.split('/')[-2]  # Extract ID from /reservation/X/edit
                    print(f"   ✓ Found Santiago's reservation with ID: {reservation_id}")
                    break
    
    if not reservation_id:
        print("   ❌ Santiago's reservation not found")
        return False
    
    # Step 2: Get the edit form
    print("2. Loading edit form...")
    edit_url = f"{base_url}/reservation/{reservation_id}/edit"
    edit_response = session.get(edit_url)
    
    if edit_response.status_code != 200:
        print(f"   ❌ Cannot access edit form: {edit_response.status_code}")
        return False
    
    # Parse form and get CSRF token
    soup = BeautifulSoup(edit_response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_token:
        print("   ❌ CSRF token not found in edit form")
        return False
    
    csrf_value = csrf_token.get('value')
    print(f"   ✓ Edit form loaded, CSRF: {csrf_value[:20]}...")
    
    # Get current cliente value
    cliente_field = soup.find('input', {'name': 'cliente'})
    current_cliente = cliente_field.get('value') if cliente_field else 'Unknown'
    print(f"   ✓ Current cliente: {current_cliente}")
    
    # Step 3: Submit edit with new name
    print("3. Submitting edit form...")
    new_name = "Santiago China"
    
    # Prepare form data - keep all existing values and only change cliente
    form_data = {
        'csrf_token': csrf_value,
        'cliente': new_name,
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
    }
    
    edit_response = session.post(edit_url, data=form_data, allow_redirects=False)
    print(f"   Status: {edit_response.status_code}")
    
    if edit_response.status_code != 302:
        print(f"   ❌ Edit failed - expected redirect, got {edit_response.status_code}")
        print(f"   Response: {edit_response.text[:200]}...")
        return False
    
    print("   ✓ Edit submitted successfully (redirect received)")
    
    # Step 4: Verify the change was saved
    print("4. Verifying changes were saved...")
    
    # Check reservations list
    reservations_response = session.get(f"{base_url}/reservations")
    if reservations_response.status_code != 200:
        print("   ❌ Cannot access reservations after edit")
        return False
    
    content = reservations_response.text
    if new_name in content:
        print(f"   ✅ SUCCESS: '{new_name}' found in reservations list")
        return True
    else:
        print(f"   ❌ FAILURE: '{new_name}' NOT found in reservations list")
        print(f"   Still shows: {current_cliente}")
        
        # Check the specific reservation page too
        view_response = session.get(f"{base_url}/reservation/{reservation_id}")
        if view_response.status_code == 200:
            if new_name in view_response.text:
                print(f"   ⚠️  Found in reservation view but not in list")
            else:
                print(f"   ❌ Not found in reservation view either")
        
        return False

if __name__ == "__main__":
    success = test_santiago_edit()
    if success:
        print("\n✅ SANTIAGO EDIT TEST PASSED")
    else:
        print("\n❌ SANTIAGO EDIT TEST FAILED")
    sys.exit(0 if success else 1)