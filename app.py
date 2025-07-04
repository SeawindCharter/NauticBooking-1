import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "nauticbooking-super-secret-key-2025")
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///reservas.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'

# Create upload directory if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

with app.app_context():
    # Import models to ensure tables are created
    import models
    
    # Create all tables
    db.create_all()
    
    # Create Santiago admin user if no admin exists
    if models.Admin.query.count() == 0:
        admin = models.Admin(username='Santiago', email='santiago@nauticbooking.com')
        admin.set_password('Santiago123')
        db.session.add(admin)
        db.session.commit()
        logging.info("Santiago admin user created: Santiago/Santiago123")

    
    # Add sample reservations if none exist
    if models.Reserva.query.count() == 0:
        from datetime import datetime, timedelta
        
        # Sample reservation 1
        reserva1 = models.Reserva(
            cliente='Juan Pérez',
            email_cliente='juan@example.com',
            telefono_cliente='+34 600 123 456',
            barco='Oceanis 51.1',
            fecha_checkin=datetime.now() + timedelta(days=30),
            fecha_checkout=datetime.now() + timedelta(days=37),
            precio_total=2800.00,
            pago_a=1400.00,
            pago_b=1400.00,
            apa=500.00,
            codigo_promocional='SUMMER2024',
            descuento=140.00,
            extras='Patrón profesional, equipo de snorkel',
            extras_facturados=300.00,
            observaciones='Cliente VIP, check-in flexible'
        )
        
        # Sample reservation 2  
        reserva2 = models.Reserva(
            cliente='María González',
            email_cliente='maria@example.com',
            telefono_cliente='+34 666 987 654',
            barco='Lagoon 42',
            fecha_checkin=datetime.now() + timedelta(days=60),
            fecha_checkout=datetime.now() + timedelta(days=65),
            precio_total=2200.00,
            pago_a=1100.00,
            pago_b=1100.00,
            apa=400.00,
            extras='Kayak, tabla de paddle surf',
            extras_facturados=150.00,
            observaciones='Aniversario de bodas'
        )
        
        db.session.add(reserva1)
        db.session.add(reserva2)
        db.session.commit()
        logging.info("Sample reservations created")

# Register blueprints at the end to avoid circular imports
def register_blueprints():
    from routes import main_bp
    from admin_routes import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

register_blueprints()
