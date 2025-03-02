import sys
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    Role, User, Enrollment, LectureSession,
    Assignment, Submission, Notification, Class
)
from werkzeug.security import generate_password_hash

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
        admin = User(username='admin', email='admin@example.com', password_hash=generate_password_hash('123'))
        admin.roles.append(Role.query.filter_by(name='admin').first())
        db.session.add(admin)
    # Lecturer
    lecturer1 = User.query.filter_by(username='lecturer1').first()
    if not lecturer1:
        lecturer1 = User(username='lecturer1', email='lecturer1@example.com', password_hash=generate_password_hash('123'))
        lecturer1.roles.append(Role.query.filter_by(name='lecturer').first())
        db.session.add(lecturer1)
    lecturer2 = User.query.filter_by(username='lecturer2').first()
    if not lecturer2:
        lecturer2 = User(username='lecturer2', email='lecturer2@example.com', password_hash=generate_password_hash('123'))
        lecturer2.roles.append(Role.query.filter_by(name='lecturer').first())
        db.session.add(lecturer2)
    lecturer3 = User.query.filter_by(username='lecturer3').first()
    if not lecturer3:
        lecturer3 = User(username='lecturer3', email='lecturer3@example.com', password_hash=generate_password_hash('123'))
        lecturer3.roles.append(Role.query.filter_by(name='lecturer').first())
        db.session.add(lecturer3)
    # Students
    student1 = User.query.filter_by(username='student1').first()
    if not student1:
        student1 = User(username='student1', email='student1@example.com', password_hash=generate_password_hash('123'))
        student1.roles.append(Role.query.filter_by(name='student').first())
        db.session.add(student1)
    student2 = User.query.filter_by(username='student2').first()
    if not student2:
        student2 = User(username='student2', email='student2@example.com', password_hash=generate_password_hash('123'))
        student2.roles.append(Role.query.filter_by(name='student').first())
        db.session.add(student2)
    student3 = User.query.filter_by(username='student3').first()
    if not student3:
        student3 = User(username='student3', email='student3@example.com', password_hash=generate_password_hash('123'))
        student3.roles.append(Role.query.filter_by(name='student').first())
        db.session.add(student3)
    db.session.commit()
    print("Users created.")

    # Tạo lớp học
    class1 = Class.query.filter_by(name='Class 1').first()
    if not class1:
        class1 = Class(
            name='Class 1',
            description='This is a sample class 1.',
            created_on=datetime.utcnow()
        )
        db.session.add(class1)
    class2 = Class.query.filter_by(name='Class 2').first()
    if not class2:
        class2 = Class(
            name='Class 2',
            description='This is a sample class 2.',
            created_on=datetime.utcnow()
        )
        db.session.add(class2)
    class3 = Class.query.filter_by(name='Class 3').first()
    if not class3:
        class3 = Class(
            name='Class 3',
            description='This is a sample class 3.',
            created_on=datetime.utcnow()
        )
        db.session.add(class3)
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
    enrollment3 = Enrollment.query.filter_by(student_id=student3.id, class_id=class2.id).first()
    if not enrollment3:
        enrollment3 = Enrollment(
            student_id=student3.id,
            class_id=class2.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment3)
    enrollment4 = Enrollment.query.filter_by(student_id=student1.id, class_id=class3.id).first()
    if not enrollment4:
        enrollment4 = Enrollment(
            student_id=student1.id,
            class_id=class3.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment4)
    enrollment5 = Enrollment.query.filter_by(student_id=student2.id, class_id=class3.id).first()
    if not enrollment5:
        enrollment5 = Enrollment(
            student_id=student2.id,
            class_id=class3.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment5)
    db.session.commit()
    print("Enrollments created.")

    # Tạo bài tập (Assignment)
    assignment1 = Assignment.query.filter_by(title='Assignment 1', class_id=class1.id).first()
    if not assignment1:
        assignment1 = Assignment(
            title='Assignment 1',
            description='This is assignment 1.',
            due_date=datetime.utcnow() + timedelta(days=7),
            class_id=class1.id,
            lecturer_id=lecturer1.id,
            class_link='http://example.com/classroom1',
            attachment_url=None
        )
        db.session.add(assignment1)
    assignment2 = Assignment.query.filter_by(title='Assignment 2', class_id=class2.id).first()
    if not assignment2:
        assignment2 = Assignment(
            title='Assignment 2',
            description='This is assignment 2.',
            due_date=datetime.utcnow() + timedelta(days=10),
            class_id=class2.id,
            lecturer_id=lecturer2.id,
            class_link='http://example.com/classroom2',
            attachment_url=None
        )
        db.session.add(assignment2)
    assignment3 = Assignment.query.filter_by(title='Assignment 3', class_id=class3.id).first()
    if not assignment3:
        assignment3 = Assignment(
            title='Assignment 3',
            description='This is assignment 3.',
            due_date=datetime.utcnow() + timedelta(days=5),
            class_id=class3.id,
            lecturer_id=lecturer3.id,
            class_link='http://example.com/classroom3',
            attachment_url=None
        )
        db.session.add(assignment3)
    db.session.commit()
    print("Assignments created.")

    # Tạo bài nộp (Submission)
    submission1 = Submission.query.filter_by(assignment_id=assignment1.id, student_id=student1.id).first()
    if not submission1:
        submission1 = Submission(
            assignment_id=assignment1.id,
            student_id=student1.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student1_assignment1.zip',
            grade=85.0,
            feedback='Good job!',
            status='graded'
        )
        db.session.add(submission1)
    submission2 = Submission.query.filter_by(assignment_id=assignment1.id, student_id=student2.id).first()
    if not submission2:
        submission2 = Submission(
            assignment_id=assignment1.id,
            student_id=student2.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student2_assignment1.zip',
            grade=90.0,
            feedback='Excellent work!',
            status='graded'
        )
        db.session.add(submission2)
    submission3 = Submission.query.filter_by(assignment_id=assignment2.id, student_id=student3.id).first()
    if not submission3:
        submission3 = Submission(
            assignment_id=assignment2.id,
            student_id=student3.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student3_assignment2.zip',
            grade=88.0,
            feedback='Well done!',
            status='graded'
        )
        db.session.add(submission3)
    submission4 = Submission.query.filter_by(assignment_id=assignment3.id, student_id=student1.id).first()
    if not submission4:
        submission4 = Submission(
            assignment_id=assignment3.id,
            student_id=student1.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student1_assignment3.zip',
            grade=92.0,
            feedback='Great job!',
            status='graded'
        )
        db.session.add(submission4)
    submission5 = Submission.query.filter_by(assignment_id=assignment3.id, student_id=student2.id).first()
    if not submission5:
        submission5 = Submission(
            assignment_id=assignment3.id,
            student_id=student2.id,
            submission_date=datetime.utcnow(),
            file_url='http://example.com/uploads/student2_assignment3.zip',
            grade=89.0,
            feedback='Good effort!',
            status='graded'
        )
        db.session.add(submission5)
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
    notification3 = Notification.query.filter_by(
        user_id=student3.id,
        message='Assignment 2 has been graded.'
    ).first()
    if not notification3:
        notification3 = Notification(
            user_id=student3.id,
            message='Assignment 2 has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification3)
    notification4 = Notification.query.filter_by(
        user_id=student1.id,
        message='Assignment 3 has been graded.'
    ).first()
    if not notification4:
        notification4 = Notification(
            user_id=student1.id,
            message='Assignment 3 has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification4)
    notification5 = Notification.query.filter_by(
        user_id=student2.id,
        message='Assignment 3 has been graded.'
    ).first()
    if not notification5:
        notification5 = Notification(
            user_id=student2.id,
            message='Assignment 3 has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification5)
    db.session.commit()
    print("Notifications created.")

    print("Sample data created successfully.")

def add_students():
    app = create_app()
    app.app_context().push()

    # Ensure the 'student' role exists
    student_role = Role.query.filter_by(name='student').first()
    if not student_role:
        student_role = Role(name='student')
        db.session.add(student_role)
        db.session.commit()

    # Add 10 new students
    for i in range(3, 13):  # Assuming student1 and student2 already exist
        username = f'student{i}'
        email = f'student{i}@example.com'
        if not User.query.filter_by(username=username).first():
            student = User(
                username=username,
                email=email,
                password_hash=generate_password_hash('123')
            )
            student.roles.append(student_role)
            db.session.add(student)

    db.session.commit()
    print("10 new students added to the database.")

if __name__ == '__main__':
    populate()
    add_students()
