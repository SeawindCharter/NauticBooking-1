#!/usr/bin/env python3
"""
Test completo de todas las rutas de navegación del sistema NauticBooking
"""

import requests
import sys

def test_route(url, description):
    """Test a single route and return result"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {description}: {url}")
            return True
        else:
            print(f"❌ {description}: {url} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {description}: {url} (Error: {str(e)})")
        return False

def main():
    base_url = "http://localhost:5000"
    
    print("=== TESTING COMPLETE NAVIGATION SYSTEM ===\n")
    
    routes_to_test = [
        # Main routes
        (f"{base_url}/", "Homepage"),
        (f"{base_url}/reservations", "Reservations List"),
        (f"{base_url}/reservation/new", "New Reservation"),
        (f"{base_url}/reservation/1", "View Reservation"),
        (f"{base_url}/reservation/1/edit", "Edit Reservation"),
        
        # Admin routes
        (f"{base_url}/admin/login", "Admin Login"),
        (f"{base_url}/admin/dashboard", "Admin Dashboard"),
        (f"{base_url}/admin/import-excel", "Import Excel"),
        (f"{base_url}/admin/promotional-codes", "Promotional Codes"),
        (f"{base_url}/admin/reports", "Reports"),
    ]
    
    working_routes = 0
    total_routes = len(routes_to_test)
    
    for url, description in routes_to_test:
        if test_route(url, description):
            working_routes += 1
    
    print(f"\n=== RESULTS ===")
    print(f"Working routes: {working_routes}/{total_routes}")
    print(f"Success rate: {(working_routes/total_routes)*100:.1f}%")
    
    if working_routes == total_routes:
        print("🎉 ALL ROUTES WORKING PERFECTLY!")
        return True
    else:
        print("⚠️  Some routes need fixing")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)