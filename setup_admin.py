# setup_admin.py
from app import db
from models import Admin

# Borra todos los admins existentes
Admin.query.delete()
db.session.commit()

# Crea sólo a Santiago
admin = Admin(username='Santiago', email='santiago@nauticbooking.com')
admin.set_password('Santiago123')
db.session.add(admin)
db.session.commit()
print("✓ Admin 'Santiago' creado con contraseña Santiago123")
