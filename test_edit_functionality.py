#!/usr/bin/env python3
"""
Test script to verify edit functionality works correctly
"""

from app import app, db
from models import Reserva
from datetime import datetime

def test_edit_functionality():
    with app.app_context():
        print("=== TESTING EDIT FUNCTIONALITY ===")
        
        # Get reservation 2 (Santiago)
        reserva = Reserva.query.get(2)
        if not reserva:
            print("Error: Reservation 2 not found")
            return
        
        print(f"Before edit:")
        print(f"  Cliente: {reserva.cliente}")
        print(f"  Email: {reserva.email_cliente}")
        print(f"  Updated: {reserva.updated_at}")
        
        # Simulate an edit
        old_updated = reserva.updated_at
        reserva.cliente = "Santiago Editado"
        reserva.email_cliente = "santiago.editado@test.com"
        reserva.updated_at = datetime.utcnow()
        
        # Explicitly add to session and commit
        db.session.add(reserva)
        db.session.commit()
        
        # Refresh from database
        db.session.refresh(reserva)
        
        print(f"\nAfter edit:")
        print(f"  Cliente: {reserva.cliente}")
        print(f"  Email: {reserva.email_cliente}")
        print(f"  Updated: {reserva.updated_at}")
        
        # Check if timestamp changed
        if reserva.updated_at != old_updated:
            print("✓ Timestamp updated correctly")
        else:
            print("✗ Timestamp NOT updated")
        
        # Test if we can read it back
        reserva_check = Reserva.query.get(2)
        if reserva_check.cliente == "Santiago Editado":
            print("✓ Edit persisted correctly")
        else:
            print("✗ Edit NOT persisted")

if __name__ == "__main__":
    test_edit_functionality()