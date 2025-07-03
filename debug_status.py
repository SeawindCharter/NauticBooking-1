#!/usr/bin/env python3
"""
Debug script to check the current status of all reservations
"""

from app import app, db
from models import Reserva

def check_reservations():
    with app.app_context():
        print("=== CURRENT RESERVATION STATUS ===")
        reservations = Reserva.query.all()
        
        for reserva in reservations:
            print(f"\nReservation ID: {reserva.id}")
            print(f"Cliente: {reserva.cliente}")
            print(f"Email: {reserva.email_cliente}")
            print(f"Telefono: {reserva.telefono_cliente}")
            print(f"Barco: {reserva.barco}")
            print(f"Created: {reserva.created_at}")
            print(f"Updated: {reserva.updated_at}")
            print("-" * 40)

if __name__ == "__main__":
    check_reservations()