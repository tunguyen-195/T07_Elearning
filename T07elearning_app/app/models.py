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


# -------------- Model Class -------------- #
class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship to Enrollment
    enrollments = db.relationship('Enrollment', back_populates='class_')

    # Quan hệ với Assignment
    assignments = db.relationship('Assignment', backref='class', lazy='dynamic')

    def __repr__(self):
        return f"<Class {self.name}>"


# -------------- Model Enrollment -------------- #
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    enrolled_on = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship to Class
    class_ = db.relationship('Class', back_populates='enrollments')

    def __repr__(self):
        return f"<Enrollment Student={self.student_id}, Class={self.class_id}>"


# -------------- Model LectureSession -------------- #
class LectureSession(db.Model):
    __tablename__ = 'lecture_sessions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    video_url = db.Column(db.String(256))  # Đường dẫn lưu trữ video bài giảng
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    def __repr__(self):
        return f"<LectureSession {self.title}>"


# -------------- Model Assignment -------------- #
class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    max_attempts = db.Column(db.Integer, default=1)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    attachment_url = db.Column(db.String(512), nullable=True)
    class_link = db.Column(db.String(256), nullable=True)  # New field for class link
    
    # New field to track the lecturer who created the assignment
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # New field to store deadline duration in minutes
    deadline_duration = db.Column(db.Integer, nullable=False, default=0)

    # Ensure the backref name does not conflict
    submissions = db.relationship('Submission', back_populates='assignment')

    def __repr__(self):
        return f"<Assignment {self.title}>"


# -------------- Model Submission -------------- #
class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_url = db.Column(db.String(512), nullable=True)
    grade = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(64), nullable=False, default='pending')
    answer = db.Column(db.Text, nullable=True)

    assignment = db.relationship('Assignment', back_populates='submissions')

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


# -------------- Model Course -------------- #
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    videos = db.relationship('LectureVideo', back_populates='course')

    def __repr__(self):
        return f"<Course {self.name}>"


# -------------- Model LectureVideo -------------- #
class LectureVideo(db.Model):
    __tablename__ = 'lecture_videos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    video_url = db.Column(db.String(512), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    course = db.relationship('Course', back_populates='videos')

    def __repr__(self):
        return f"<LectureVideo {self.title}>"