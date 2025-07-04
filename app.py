import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
app.debug = True
app.logger.setLevel(logging.DEBUG)
app.secret_key = os.environ.get("SESSION_SECRET", "nauticbooking-super-secret-key-2025")
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///reservas.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle": 300, "pool_pre_ping": True}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.query.get(int(user_id))

# Create tables and sample data
with app.app_context():
    import models
    db.create_all()
    
    # Create sample admin if it doesn't exist
    admin = models.Admin.query.filter_by(username='Santiago').first()
    if not admin:
        admin = models.Admin(
            username='Santiago',
            email='santiago@nauticbooking.com'
        )
        admin.set_password('Santiago123')
        db.session.add(admin)
        db.session.commit()
        logging.info("Sample admin created")
    
    # Create sample reservations if they don't exist
    if models.Reserva.query.count() == 0:
        from datetime import datetime, time
        reserva1 = models.Reserva(
            cliente='Juan Pérez',
            email_cliente='juan@example.com',
            telefono_cliente='+34 666 123 456',
            barco='Oceanis 51.1',
            fecha_checkin=datetime(2025, 7, 15),
            fecha_checkout=datetime(2025, 7, 22),
            hora_inicio=time(10, 0),
            hora_finalizacion=time(18, 0),
            precio_total=2500.00,
            pago_a=1200.00,
            pago_b=1300.00,
            apa=250.00,
            extras='Patrón incluido',
            observaciones='Cliente VIP'
        )
        
        reserva2 = models.Reserva(
            cliente='Santiago FINAL TEST',
            email_cliente='santiago@test.com',
            telefono_cliente='+34 600 000 000',
            barco='Oceanis 51.1',
            fecha_checkin=datetime(2025, 8, 1),
            fecha_checkout=datetime(2025, 8, 8),
            hora_inicio=time(10, 0),
            hora_finalizacion=time(18, 0),
            precio_total=3000.00,
            pago_a=1500.00,
            pago_b=1500.00,
            apa=300.00,
            extras='Final test edit',
            observaciones='Final test observation'
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