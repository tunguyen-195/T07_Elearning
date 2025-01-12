import sys
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    Role, User, Course, Enrollment, LectureSession,
    Assignment, Submission, Notification
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

    # Tạo khoá học
    course = Course.query.filter_by(name='Introduction to Flask').first()
    if not course:
        course = Course(
            name='Introduction to Flask',
            description='Learn the basics of Flask web development.',
            lecturer_id=lecturer.id,
            start_date=datetime.utcnow().date(),
            end_date=(datetime.utcnow() + timedelta(days=60)).date(),
            created_on=datetime.utcnow()
        )
        db.session.add(course)
        db.session.commit()
    print("Course created.")

    # Tạo ghi danh cho học viên
    enrollment1 = Enrollment.query.filter_by(student_id=student1.id, course_id=course.id).first()
    if not enrollment1:
        enrollment1 = Enrollment(
            student_id=student1.id,
            course_id=course.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment1)
    enrollment2 = Enrollment.query.filter_by(student_id=student2.id, course_id=course.id).first()
    if not enrollment2:
        enrollment2 = Enrollment(
            student_id=student2.id,
            course_id=course.id,
            enrolled_on=datetime.utcnow()
        )
        db.session.add(enrollment2)
    db.session.commit()
    print("Enrollments created.")

    # Tạo buổi giảng (LectureSession)
    lecture1 = LectureSession.query.filter_by(title='Flask Basics', course_id=course.id).first()
    if not lecture1:
        lecture1 = LectureSession(
            course_id=course.id,
            title='Flask Basics',
            description='Introduction to Flask framework.',
            date=datetime.utcnow() + timedelta(days=1),
            video_url='http://example.com/videos/flask_basics'
        )
        db.session.add(lecture1)
    lecture2 = LectureSession.query.filter_by(title='Flask Extensions', course_id=course.id).first()
    if not lecture2:
        lecture2 = LectureSession(
            course_id=course.id,
            title='Flask Extensions',
            description='Using extensions with Flask.',
            date=datetime.utcnow() + timedelta(days=3),
            video_url='http://example.com/videos/flask_extensions'
        )
        db.session.add(lecture2)
    db.session.commit()
    print("Lecture sessions created.")

    # Tạo bài tập (Assignment)
    assignment = Assignment.query.filter_by(title='Flask Project', course_id=course.id).first()
    if not assignment:
        assignment = Assignment(
            course_id=course.id,
            title='Flask Project',
            description='Build a web application using Flask.',
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
            file_url='http://example.com/uploads/student1_flask_project.zip',
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
            file_url='http://example.com/uploads/student2_flask_project.zip',
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
        message='Assignment Flask Project has been graded.'
    ).first()
    if not notification1:
        notification1 = Notification(
            user_id=student1.id,
            message='Assignment Flask Project has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification1)
    notification2 = Notification.query.filter_by(
        user_id=student2.id,
        message='Assignment Flask Project has been graded.'
    ).first()
    if not notification2:
        notification2 = Notification(
            user_id=student2.id,
            message='Assignment Flask Project has been graded.',
            created_on=datetime.utcnow(),
            is_read=False
        )
        db.session.add(notification2)
    db.session.commit()
    print("Notifications created.")

    print("Dữ liệu mẫu đã được chèn thành công vào cơ sở dữ liệu.")

if __name__ == '__main__':
    populate()
