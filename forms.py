from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    StringField, TextAreaField, FloatField,
    DateField, TimeField, SelectField,
    PasswordField, BooleanField
)
from wtforms.validators import (
    DataRequired, Email, Optional, NumberRange,
    Length, ValidationError
)
from datetime import time
from models import CodigoPromocional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')

class ReservaForm(FlaskForm):
    # Datos de cliente
    cliente            = StringField('Nombre del Cliente', validators=[DataRequired(), Length(max=100)])
    email_cliente      = StringField('Email del Cliente', validators=[Optional(), Email(), Length(max=120)])
    telefono_cliente   = StringField('Teléfono del Cliente', validators=[Optional(), Length(max=20)])
    client_type        = SelectField(
        'Tipo de Cliente',
        choices=[('Particular','Particular'),('Empresa','Empresa'),('Broker','Broker')],
        default='Particular', validators=[DataRequired()]
    )
    broker             = StringField('Broker / Intermediario', validators=[Optional(), Length(max=100)])

    # Detalles de la reserva
    barco              = StringField('Barco', validators=[DataRequired(), Length(max=100)])
    fecha_checkin      = DateField('Fecha de Check-in', validators=[DataRequired()])
    fecha_checkout     = DateField('Fecha de Check-out', validators=[DataRequired()])
    hora_inicio        = TimeField('Hora de Inicio', validators=[Optional()], default=time(10, 0))
    hora_finalizacion  = TimeField('Hora de Finalización', validators=[Optional()], default=time(18, 0))

    # Tarifas y pagos
    precio_total       = FloatField('Precio Total (€)', validators=[DataRequired(), NumberRange(min=0)])
    pago_a             = FloatField('Pago A (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    pago_b             = FloatField('Pago B (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    apa                = FloatField('APA (€)', validators=[Optional(), NumberRange(min=0)], default=0)

    # Comisión de broker
    commission_rate    = FloatField(
        'Comisión Broker (%)',
        validators=[Optional(), NumberRange(min=0, max=100)],
        default=0
    )
    commission_paid_a  = FloatField('Comisión Pagada A (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    commission_paid_b  = FloatField('Comisión Pagada B (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    commission_status  = SelectField(
        'Estado Comisión',
        choices=[
            ('Pendiente','Pendiente'),
            ('Pagado A','Pagado A'),
            ('Pagado B','Pagado B'),
            ('Pagado Total','Pagado Total')
        ],
        default='Pendiente'
    )

    # Códigos y extras
    codigo_promocional = StringField('Código Promocional', validators=[Optional(), Length(max=50)])
    extras             = TextAreaField('Extras', validators=[Optional(), Length(max=500)])
    extras_facturados  = FloatField('Extras Facturados (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    observaciones      = TextAreaField('Observaciones', validators=[Optional(), Length(max=1000)])

    # Cancelación
    is_cancelled       = BooleanField('Reserva Cancelada')
    cancellation_date  = DateField('Fecha Cancelación', validators=[Optional()])
    cancellation_reason= TextAreaField('Motivo Cancelación', validators=[Optional(), Length(max=500)])
    cancellation_fee   = FloatField('Cargo Cancelación (€)', validators=[Optional(), NumberRange(min=0)], default=0)

    # Validaciones propias
    def validate_fecha_checkout(self, field):
        if field.data <= self.fecha_checkin.data:
            raise ValidationError('La fecha de check-out debe ser posterior a la fecha de check-in.')

    def validate_codigo_promocional(self, field):
        if field.data:
            codigo = CodigoPromocional.query.filter_by(codigo=field.data.upper()).first()
            if not codigo or not codigo.is_valid():
                raise ValidationError('El código promocional no es válido o ha expirado.')

class ImportExcelForm(FlaskForm):
    file = FileField('Archivo Excel', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Solo se permiten archivos Excel (.xlsx, .xls)')
    ])

class SearchForm(FlaskForm):
    search_term = StringField('Buscar', validators=[Optional()])
    search_type = SelectField('Buscar por', choices=[
        ('cliente', 'Cliente'),
        ('barco', 'Barco'),
        ('codigo_promocional', 'Código Promocional')
    ], default='cliente')
