from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime
from app import db
from models import Admin, Reserva, CodigoPromocional
from forms import LoginForm, ImportExcelForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin, remember=form.remember_me.data)
            flash('Bienvenido al panel de administración', 'success')
            # Force a complete page reload to ensure proper redirection
            return redirect(url_for('admin.dashboard'))
        flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Statistics for dashboard
    total_reservations = Reserva.query.count()
    total_revenue = db.session.query(db.func.sum(Reserva.precio_total)).scalar() or 0
    total_paid = db.session.query(db.func.sum(Reserva.pago_a + Reserva.pago_b)).scalar() or 0
    pending_balance = total_revenue - total_paid
    
    # Recent reservations
    recent_reservations = Reserva.query.order_by(Reserva.created_at.desc()).limit(10).all()
    
    # Upcoming check-ins
    upcoming_checkins = Reserva.query.filter(
        Reserva.fecha_checkin >= datetime.now()
    ).order_by(Reserva.fecha_checkin.asc()).limit(5).all()
    
    # Monthly revenue data for chart - PostgreSQL compatible
    monthly_revenue_query = db.session.query(
        db.func.to_char(Reserva.fecha_checkin, 'YYYY-MM').label('month'),
        db.func.sum(Reserva.precio_total).label('revenue')
    ).group_by('month').order_by('month').all()
    
    # Convert to JSON serializable format
    monthly_revenue = [{'month': row.month, 'revenue': float(row.revenue or 0)} for row in monthly_revenue_query]
    
    return render_template('admin/dashboard.html',
                         total_reservations=total_reservations,
                         total_revenue=total_revenue,
                         total_paid=total_paid,
                         pending_balance=pending_balance,
                         recent_reservations=recent_reservations,
                         upcoming_checkins=upcoming_checkins,
                         monthly_revenue=monthly_revenue)

@admin_bp.route('/import-excel', methods=['GET', 'POST'])
@login_required
def import_excel():
    form = ImportExcelForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Read Excel file
                df = pd.read_excel(filepath)
                
                # Process and validate data
                imported_count = 0
                errors = []
                
                for index, row in df.iterrows():
                    try:
                        # Map Excel columns to database fields
                        # Adjust column names based on your Excel structure
                        reserva = Reserva(
                            cliente=str(row.get('Cliente', '')),
                            email_cliente=str(row.get('Email', '')) if pd.notna(row.get('Email')) else None,
                            telefono_cliente=str(row.get('Telefono', '')) if pd.notna(row.get('Telefono')) else None,
                            barco=str(row.get('Barco', '')),
                            fecha_checkin=pd.to_datetime(row.get('Check-in')),
                            fecha_checkout=pd.to_datetime(row.get('Check-out')),
                            precio_total=float(row.get('Precio Total', 0)),
                            pago_a=float(row.get('Pago A', 0)),
                            pago_b=float(row.get('Pago B', 0)),
                            apa=float(row.get('APA', 0)),
                            codigo_promocional=str(row.get('Codigo Promocional', '')) if pd.notna(row.get('Codigo Promocional')) else None,
                            descuento=float(row.get('Descuento', 0)),
                            extras=str(row.get('Extras', '')) if pd.notna(row.get('Extras')) else None,
                            extras_facturados=float(row.get('Extras Facturados', 0)),
                            observaciones=str(row.get('Observaciones', '')) if pd.notna(row.get('Observaciones')) else None
                        )
                        
                        db.session.add(reserva)
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f"Fila {index + 2}: {str(e)}")
                
                if imported_count > 0:
                    db.session.commit()
                    flash(f'{imported_count} reservas importadas exitosamente', 'success')
                
                if errors:
                    flash(f'Errores encontrados: {"; ".join(errors[:5])}', 'warning')
                
                # Clean up uploaded file
                os.remove(filepath)
                
            except Exception as e:
                flash(f'Error al procesar el archivo: {str(e)}', 'error')
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    return render_template('admin/import_excel.html', form=form)

@admin_bp.route('/promotional-codes')
@login_required
def promotional_codes():
    codes = CodigoPromocional.query.order_by(CodigoPromocional.created_at.desc()).all()
    return render_template('admin/promotional_codes.html', codes=codes)

@admin_bp.route('/reports')
@login_required
def reports():
    # Generate various reports
    
    # Revenue by month
    monthly_revenue = db.session.query(
        db.func.strftime('%Y-%m', Reserva.fecha_checkin).label('month'),
        db.func.sum(Reserva.precio_total).label('revenue'),
        db.func.count(Reserva.id).label('reservations')
    ).group_by('month').order_by('month').all()
    
    # Popular boats
    popular_boats = db.session.query(
        Reserva.barco,
        db.func.count(Reserva.id).label('reservations'),
        db.func.sum(Reserva.precio_total).label('revenue')
    ).group_by(Reserva.barco).order_by(db.func.count(Reserva.id).desc()).all()
    
    # Payment status
    payment_status = db.session.query(
        db.func.sum(Reserva.precio_total).label('total_revenue'),
        db.func.sum(Reserva.pago_a + Reserva.pago_b).label('total_paid')
    ).first()
    
    return render_template('admin/reports.html',
                         monthly_revenue=monthly_revenue,
                         popular_boats=popular_boats,
                         payment_status=payment_status)
