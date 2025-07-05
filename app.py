import os
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

# Inicializa extensiones
db = SQLAlchemy()
login_manager = LoginManager()

# Crea y configura la app
app = Flask(__name__)
app.debug = True
app.logger.setLevel(logging.DEBUG)
app.secret_key = os.environ.get("SESSION_SECRET", "nauticbooking-super-secret-key-2025")
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# --- FORZAR USO DE SQLITE LOCAL ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reservas.db"
# -----------------------------------

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Inicializa extensiones
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'

# Importa modelos y crea tablas a la primera
with app.app_context():
    import models
    db.create_all()

# Cargo tu blueprint de rutas
from routes import main_bp
from admin_routes import admin_bp
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
