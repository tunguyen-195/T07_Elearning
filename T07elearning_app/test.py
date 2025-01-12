from app import db
from app.models import User

# Kiểm tra người dùng admin
admin = User.query.filter_by(username='admin').first()
print(admin)
print(admin.email)
print(admin.check_password('123'))  # Nên in ra True
print(admin.check_password('wrongpassword'))  # Nên in ra False
