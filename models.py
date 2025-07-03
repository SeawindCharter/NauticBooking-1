from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    email_cliente = db.Column(db.String(120))
    telefono_cliente = db.Column(db.String(20))
    barco = db.Column(db.String(100), nullable=False)
    fecha_checkin = db.Column(db.DateTime, nullable=False)
    fecha_checkout = db.Column(db.DateTime, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)
    pago_a = db.Column(db.Float, default=0.0)
    pago_b = db.Column(db.Float, default=0.0)
    apa = db.Column(db.Float, default=0.0)
    codigo_promocional = db.Column(db.String(50))
    descuento = db.Column(db.Float, default=0.0)
    extras = db.Column(db.Text)
    extras_facturados = db.Column(db.Float, default=0.0)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def total_pagado(self):
        return (self.pago_a or 0) + (self.pago_b or 0)
    
    @property
    def balance_pendiente(self):
        return self.precio_total - self.total_pagado
    
    @property
    def duracion_dias(self):
        return (self.fecha_checkout - self.fecha_checkin).days
    
    def __repr__(self):
        return f'<Reserva {self.cliente} - {self.barco}>'

class CodigoPromocional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descuento_porcentaje = db.Column(db.Float, default=0.0)
    descuento_fijo = db.Column(db.Float, default=0.0)
    activo = db.Column(db.Boolean, default=True)
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    usos_maximos = db.Column(db.Integer)
    usos_actuales = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        if not self.activo:
            return False
        
        now = datetime.utcnow()
        if self.fecha_inicio and now < self.fecha_inicio:
            return False
        if self.fecha_fin and now > self.fecha_fin:
            return False
        if self.usos_maximos and self.usos_actuales >= self.usos_maximos:
            return False
        
        return True
    
    def calcular_descuento(self, precio):
        if not self.is_valid():
            return 0.0
        
        if self.descuento_porcentaje > 0:
            return precio * (self.descuento_porcentaje / 100)
        else:
            return min(self.descuento_fijo, precio)
