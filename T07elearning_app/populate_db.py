import sys
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    Role, User, Enrollment, LectureSession,
    Assignment, Submission, Notification, Class
)

def populate():
    # Tạo app context
    app = create_app()
    app.app_context().push()

    # Xoá & tạo lại toàn bộ database (nên cẩn thận trong production)
    db.drop_all()
    db.create_all()

    # Tạo các vai trò
    roles = ['student', 'lecturer', 'admin']
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()
    print("Roles created.")

    # Tạo người dùng mẫu
    # Admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('123')
        admin.roles.append(Role.query.filter_by(name='admin').first())
        db.session.add(admin)
    # Lecturer
    lecturer = User.query.filter_by(username='lecturer1').first()
    if not lecturer:
        lecturer = User(username='lecturer1', email='lecturer1@example.com')
        lecturer.set_password('123')
        lecturer.roles.append(Role.query.filter_by(name='lecturer').first())
        db.session.add(lecturer)
    # Students
    student1 = User.query.filter_by(username='student1').first()
    if not student1:
        student1 = User(username='student1', email='student1@example.com')
        student1.set_password('123')
        student1.roles.append(Role.query.filter_by(name='student').first())
        db.session.add(student1)
    student2 = User.query.filter_by(username='student2').first()
    if not student2:
        student2 = User(username='student2', email='student2@example.com')
        student2.set_password('123')
        student2.roles.append(Role.query.filter_by(name='student').first())
        db.session.add(student2)
    db.session.commit()
    print("Users created.")

    # Tạo lớp học
    class1 = Class.query.filter_by(name='Class 1').first()
    if not class1:
        class1 = Class(
            name='Class 1',
            description='Description for Class 1',
            created_on=datetime.utcnow()
        )
        db.session.add(class1)
    db.session.commit()
    print("Classes created.")

    # Tạo ghi danh cho học viên
    enrollment1 = Enrollment.query.filter_by(student_id=student1.id, class_id=class1.id).first()
    if not enrollment1:
        enrollment1 = Enrollment(
            student_id=student1.id,
            class_id=class1.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment1)
    enrollment2 = Enrollment.query.filter_by(student_id=student2.id, class_id=class1.id).first()
    if not enrollment2:
        enrollment2 = Enrollment(
            student_id=student2.id,
            class_id=class1.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment2)
    db.session.commit()
    print("Enrollments created.")

    # Tạo buổi giảng (LectureSession)
    lecture1 = LectureSession.query.filter_by(title='Lecture 1', class_id=class1.id).first()
    if not lecture1:
        lecture1 = LectureSession(
            class_id=class1.id,
            title='Lecture 1',
            description='Introduction to the course.',
            date=datetime.utcnow() + timedelta(days=1),
            video_url='http://example.com/videos/lecture1'
        )
        db.session.add(lecture1)
    db.session.commit()
    print("Lecture sessions created.")

    # Tạo bài tập (Assignment)
    assignment = Assignment.query.filter_by(title='Assignment 1', class_id=class1.id).first()
    if not assignment:
        assignment = Assignment(
            class_id=class1.id,
            title='Assignment 1',
            description='Complete the assignment.',
            due_date=datetime.utcnow() + timedelta(days=30),
            max_attempts=3,
            created_on=datetime.utcnow()
        )
        db.session.add(assignment)
    db.session.commit()
    print("Assignments created.")

    # Tạo bài nộp (Submission)
    submission1 = Submission.query.filter_by(assignment_id=assignment.id, student_id=student1.id).first()
    if not submission1:
        submission1 = Submission(
            assignment_id=assignment.id,
            student_id=student1.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student1_assignment.zip',
            grade=85.0,
            feedback='Good job!',
            status='graded'
        )
        db.session.add(submission1)
    submission2 = Submission.query.filter_by(assignment_id=assignment.id, student_id=student2.id).first()
    if not submission2:
        submission2 = Submission(
            assignment_id=assignment.id,
            student_id=student2.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student2_assignment.zip',
            grade=90.0,
            feedback='Excellent work!',
            status='graded'
        )
        db.session.add(submission2)
    db.session.commit()
    print("Submissions created.")

    # Tạo thông báo (Notification)
    notification1 = Notification.query.filter_by(
        user_id=student1.id,
        message='Assignment 1 has been graded.'
    ).first()
    if not notification1:
        notification1 = Notification(
            user_id=student1.id,
            message='Assignment 1 has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification1)
    notification2 = Notification.query.filter_by(
        user_id=student2.id,
        message='Assignment 1 has been graded.'
    ).first()
    if not notification2:
        notification2 = Notification(
            user_id=student2.id,
            message='Assignment 1 has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification2)
    db.session.commit()
    print("Notifications created.")

if __name__ == '__main__':
    populate()
