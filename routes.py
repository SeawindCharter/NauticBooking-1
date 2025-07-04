from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from models import Reserva, CodigoPromocional
from forms import ReservaForm, SearchForm
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/diagnostico')
def diagnostico():
    return render_template('diagnostico.html')

@main_bp.route('/test')
def test_simple():
    return render_template('test_simple.html')

@main_bp.route('/')
def index():
    recent_reservations = Reserva.query.order_by(Reserva.created_at.desc()).limit(5).all()
    total_reservations = Reserva.query.count()
    total_revenue = db.session.query(db.func.sum(Reserva.precio_total)).scalar() or 0
    pending_balance = db.session.query(
        db.func.sum(Reserva.precio_total - Reserva.pago_a - Reserva.pago_b)
    ).scalar() or 0

    return render_template(
        'index.html',
        recent_reservations=recent_reservations,
        total_reservations=total_reservations,
        total_revenue=total_revenue,
        pending_balance=pending_balance
    )

@main_bp.route('/reservations')
def reservations():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Reserva.query
    search_term = request.args.get('search_term')
    search_type = request.args.get('search_type', 'cliente')

    if search_term:
        if search_type == 'cliente':
            query = query.filter(Reserva.cliente.contains(search_term))
        elif search_type == 'barco':
            query = query.filter(Reserva.barco.contains(search_term))
        elif search_type == 'codigo_promocional':
            query = query.filter(Reserva.codigo_promocional.contains(search_term))

    reservations = query.order_by(
        Reserva.fecha_checkin.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'reservations.html',
        reservations=reservations,
        search_form=search_form,
        search_term=search_term,
        search_type=search_type
    )

@main_bp.route('/reservation/new', methods=['GET', 'POST'])
@main_bp.route('/reservation/create', methods=['GET', 'POST'])
def create_reservation():
    form = ReservaForm()
    if form.validate_on_submit():
        # Aplicar descuento promocional si corresponde
        descuento = 0.0
        if form.codigo_promocional.data:
            codigo = CodigoPromocional.query.filter_by(
                codigo=form.codigo_promocional.data.upper()
            ).first()
            if codigo and codigo.is_valid():
                descuento = codigo.calcular_descuento(form.precio_total.data)
                codigo.usos_actuales += 1
                db.session.commit()

        # Crear la reserva
        reserva = Reserva(
            cliente=form.cliente.data,
            email_cliente=form.email_cliente.data,
            telefono_cliente=form.telefono_cliente.data,
            barco=form.barco.data,
            fecha_checkin=form.fecha_checkin.data,
            fecha_checkout=form.fecha_checkout.data,
            hora_inicio=form.hora_inicio.data,
            hora_finalizacion=form.hora_finalizacion.data,
            precio_total=form.precio_total.data,
            pago_a=form.pago_a.data or 0,
            pago_b=form.pago_b.data or 0,
            apa=form.apa.data or 0,
            codigo_promocional=(
                form.codigo_promocional.data.upper()
                if form.codigo_promocional.data else None
            ),
            descuento=descuento,
            extras=form.extras.data,
            extras_facturados=form.extras_facturados.data or 0,
            observaciones=form.observaciones.data
        )
        db.session.add(reserva)
        db.session.commit()

        flash('Reserva creada exitosamente', 'success')
        return redirect(url_for('main.reservations'))

    # Si GET o validación falla, renderizar formulario
    return render_template('create_reservation.html', form=form)

@main_bp.route('/reservation/<int:id>/edit', methods=['GET', 'POST'])
def edit_reservation(id):
    reserva = Reserva.query.get_or_404(id)
    if request.method == 'GET':
        form = ReservaForm(obj=reserva)
        if reserva.fecha_checkin:
            form.fecha_checkin.data = reserva.fecha_checkin.date()
        if reserva.fecha_checkout:
            form.fecha_checkout.data = reserva.fecha_checkout.date()
    else:
        form = ReservaForm()

    if form.validate_on_submit():
        reserva.cliente = form.cliente.data
        reserva.email_cliente = form.email_cliente.data
        reserva.telefono_cliente = form.telefono_cliente.data
        reserva.barco = form.barco.data
        if form.fecha_checkin.data:
            reserva.fecha_checkin = datetime.combine(
                form.fecha_checkin.data,
                form.hora_inicio.data or datetime.min.time()
            )
        if form.fecha_checkout.data:
            reserva.fecha_checkout = datetime.combine(
                form.fecha_checkout.data,
                form.hora_finalizacion.data or datetime.min.time()
            )
        reserva.hora_inicio = form.hora_inicio.data or reserva.hora_inicio
        reserva.hora_finalizacion = form.hora_finalizacion.data or reserva.hora_finalizacion
        reserva.precio_total = form.precio_total.data
        reserva.pago_a = form.pago_a.data or 0
        reserva.pago_b = form.pago_b.data or 0
        reserva.apa = form.apa.data or 0
        reserva.codigo_promocional = (
            form.codigo_promocional.data.upper()
            if form.codigo_promocional.data else None
        )
        reserva.descuento = reserva.descuento
        reserva.extras = form.extras.data
        reserva.extras_facturados = form.extras_facturados.data or 0
        reserva.observaciones = form.observaciones.data
        reserva.updated_at = datetime.utcnow()

        db.session.add(reserva)
        db.session.commit()

        flash('Reserva actualizada exitosamente', 'success')
        return redirect(url_for('main.reservations'))

    return render_template('edit_reservation.html', form=form, reserva=reserva)

@main_bp.route('/reservation/<int:id>/delete', methods=['POST'])
def delete_reservation(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()
    flash('Reserva eliminada exitosamente', 'success')
    return redirect(url_for('main.reservations'))

@main_bp.route('/reservation/<int:id>')
def view_reservation(id):
    reserva = Reserva.query.get_or_404(id)
    return render_template('view_reservation.html', reserva=reserva)
