from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, DateField, TimeField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length, ValidationError
from datetime import datetime, time
from models import CodigoPromocional

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')

class ReservaForm(FlaskForm):
    cliente = StringField('Nombre del Cliente', validators=[DataRequired(), Length(max=100)])
    email_cliente = StringField('Email del Cliente', validators=[Optional(), Email(), Length(max=120)])
    telefono_cliente = StringField('Teléfono del Cliente', validators=[Optional(), Length(max=20)])
    barco = SelectField('Barco', choices=[
        ('Oceanis 51.1', 'Oceanis 51.1'),
        ('Lagoon 42', 'Lagoon 42'),
        ('Bavaria 46', 'Bavaria 46'),
        ('Jeanneau 54', 'Jeanneau 54'),
        ('Beneteau 62', 'Beneteau 62'),
        ('Catana 53', 'Catana 53'),
        ('Fountaine Pajot 47', 'Fountaine Pajot 47'),
        ('Leopard 45', 'Leopard 45')
    ], validators=[DataRequired()])
    fecha_checkin = DateField('Fecha de Check-in', validators=[DataRequired()])
    fecha_checkout = DateField('Fecha de Check-out', validators=[DataRequired()])
    hora_inicio = TimeField('Hora de Inicio', validators=[Optional()], default=time(10, 0))
    hora_finalizacion = TimeField('Hora de Finalización', validators=[Optional()], default=time(18, 0))
    precio_total = FloatField('Precio Total (€)', validators=[DataRequired(), NumberRange(min=0)])
    pago_a = FloatField('Pago A (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    pago_b = FloatField('Pago B (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    apa = FloatField('APA (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    codigo_promocional = StringField('Código Promocional', validators=[Optional(), Length(max=50)])
    extras = TextAreaField('Extras', validators=[Optional(), Length(max=500)])
    extras_facturados = FloatField('Extras Facturados (€)', validators=[Optional(), NumberRange(min=0)], default=0)
    observaciones = TextAreaField('Observaciones', validators=[Optional(), Length(max=1000)])
    
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
