# create_temp_db.py
from app import create_app
from app.extensions import db
from app.models import User, Role, Course, Enrollment, LectureSession, Assignment, Submission, Notification

app = create_app()

with app.app_context():
    db.create_all()
    # Bạn có thể thêm dữ liệu mẫu ở đây nếu cần
