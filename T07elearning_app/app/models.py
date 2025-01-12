from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# -------------------- Bảng phụ user_roles -------------------- #
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# -------------- Model Role -------------- #
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)  # 'student', 'lecturer', 'admin'

    users = db.relationship('User', secondary='user_roles', back_populates='roles')

    def __repr__(self):
        return f"<Role {self.name}>"


# -------------- Model User -------------- #
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ với Role
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

    # Quan hệ với Course (giảng viên)
    courses = db.relationship('Course', backref='lecturer', lazy='dynamic')

    # Quan hệ với Enrollment (học viên)
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')

    # Quan hệ với Submission (học viên)
    submissions = db.relationship('Submission', backref='student', lazy='dynamic')

    # Quan hệ với Notification
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return any(role.name == 'admin' for role in self.roles)

    def is_lecturer(self):
        return any(role.name == 'lecturer' for role in self.roles)

    def is_student(self):
        return any(role.name == 'student' for role in self.roles)

    def __repr__(self):
        return f"<User {self.username}>"


# -------------- Model Course -------------- #
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ với Enrollment
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')

    # Quan hệ với LectureSession
    lecture_sessions = db.relationship('LectureSession', backref='course', lazy='dynamic')

    # Quan hệ với Assignment
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic')

    def __repr__(self):
        return f"<Course {self.name}>"


# -------------- Model Enrollment -------------- #
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Enrollment Student={self.student_id}, Course={self.course_id}>"


# -------------- Model LectureSession -------------- #
class LectureSession(db.Model):
    __tablename__ = 'lecture_sessions'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    video_url = db.Column(db.String(256))  # Đường dẫn lưu trữ video bài giảng

    def __repr__(self):
        return f"<LectureSession {self.title}>"


# -------------- Model Assignment -------------- #
class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    max_attempts = db.Column(db.Integer, default=1)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ với Submission
    submissions = db.relationship('Submission', backref='assignment', lazy='dynamic')

    def __repr__(self):
        return f"<Assignment {self.title}>"


# -------------- Model Submission -------------- #
class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_url = db.Column(db.String(256))  # Đường dẫn đến file bài làm
    grade = db.Column(db.Float)
    feedback = db.Column(db.Text)
    status = db.Column(db.String(20), default='submitted')  # 'submitted', 'graded'

    def __repr__(self):
        return f"<Submission Assignment={self.assignment_id}, Student={self.student_id}>"


# -------------- Model Notification -------------- #
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification User={self.user_id}, Read={self.is_read}>"