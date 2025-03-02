# app/lecturer/routes.py
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from app.lecturer import bp
from app.models import Enrollment, Assignment, Class, User, Submission, Course, LectureVideo
from app.lecturer.forms import CreateAssignmentForm, AssignmentForm, CreateClassForm, EnrollStudentsForm, CreateCourseForm, UploadVideoForm
from app.extensions import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pandas as pd


@bp.route('/assignment/create', methods=['GET', 'POST'])
@login_required
def create_assignment():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))
    
    form = CreateAssignmentForm()
    if form.validate_on_submit():
        # Handle file upload
        attachment = form.attachment.data
        attachment_path = None
        if attachment:
            attachment_path = os.path.join('app', 'static', 'uploads', secure_filename(attachment.filename))
            attachment.save(attachment_path)
            attachment_url = f"uploads/{secure_filename(attachment.filename)}"

        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,  # Ensure this is a datetime object
            class_id=form.class_id.data,
            attachment_url=attachment_url,
            lecturer_id=current_user.id,  # Set the lecturer_id to the current user
            class_link=form.class_link.data  # Save the class link
        )
        db.session.add(assignment)
        db.session.commit()

        # Assign the assignment to all students in the class
        class_ = Class.query.get(form.class_id.data)
        for enrollment in class_.enrollments:
            submission = Submission(
                student_id=enrollment.student_id,
                assignment_id=assignment.id,
                status='pending'
            )
            db.session.add(submission)
        db.session.commit()

        flash('Bài tập đã được tạo và giao cho lớp thành công!')
        return redirect(url_for('lecturer.dashboard'))
    
    return render_template('lecturer/create_assignment.html', form=form)

@bp.route('/class/create', methods=['GET', 'POST'])
@login_required
def create_class():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))
    
    form = CreateClassForm()
    if form.validate_on_submit():
        new_class = Class(name=form.name.data, description=form.description.data)
        db.session.add(new_class)
        db.session.commit()
        flash('Lớp học đã được tạo thành công!')
        return redirect(url_for('lecturer.enroll_students', class_id=new_class.id))
    
    return render_template('lecturer/create_class.html', form=form)

@bp.route('/class/enroll/<int:class_id>', methods=['GET', 'POST'])
@login_required
def enroll_students(class_id):
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))
    
    class_ = Class.query.get_or_404(class_id)
    search_query = request.args.get('search', '')
    students = User.query.filter(User.roles.any(name='student'), User.username.contains(search_query)).all()
    
    form = EnrollStudentsForm()

    if form.validate_on_submit():
        # Handle Excel file upload
        if form.excel_file.data:
            excel_file = form.excel_file.data
            df = pd.read_excel(excel_file, engine='openpyxl')

            # Assuming the Excel file has a column named 'username'
            for index, row in df.iterrows():
                username = row['username']
                student = User.query.filter_by(username=username).first()
                if student and not Enrollment.query.filter_by(student_id=student.id, class_id=class_id).first():
                    enrollment = Enrollment(student_id=student.id, class_id=class_id)
                    db.session.add(enrollment)

        # Handle individual student selection
        student_ids = request.form.getlist('students')
        for student_id in student_ids:
            if not Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first():
                enrollment = Enrollment(student_id=student_id, class_id=class_id)
                db.session.add(enrollment)

        db.session.commit()
        flash('Sinh viên đã được thêm vào lớp thành công!')
        return redirect(url_for('lecturer.dashboard'))
    
    return render_template('lecturer/enroll_students.html', class_=class_, students=students, form=form)

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))
    
    # Retrieve all classes without filtering by lecturer_id
    classes = Class.query.all()
    return render_template('lecturer/dashboard.html', classes=classes)

@bp.route('/manage_assignments', methods=['GET'])
@login_required
def manage_assignments():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    # Filter assignments by the current lecturer
    assignments = Assignment.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lecturer/manage_assignments.html', assignments=assignments)

@bp.route('/assignment/<int:assignment_id>/submissions', methods=['GET'])
@login_required
def view_submissions(assignment_id):
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = Submission.query.filter_by(assignment_id=assignment.id).all()
    return render_template('lecturer/view_submissions.html', assignment=assignment, submissions=submissions)

@bp.route('/assignment/<int:assignment_id>/grade', methods=['POST'])
@login_required
def grade_submissions(assignment_id):
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = Submission.query.filter_by(assignment_id=assignment.id).all()

    grades = request.form.getlist('grades')
    feedbacks = request.form.getlist('feedbacks')

    for submission in submissions:
        grade = request.form.get(f'grades[{submission.id}]')
        feedback = request.form.get(f'feedbacks[{submission.id}]')

        if grade:
            submission.grade = float(grade)
        if feedback:
            submission.feedback = feedback

        submission.status = 'graded' if grade else submission.status

    db.session.commit()
    flash('Đã lưu thay đổi thành công!', 'success')
    return redirect(url_for('lecturer.view_submissions', assignment_id=assignment.id))

@bp.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    # Ensure the path is correct and secure
    upload_folder = os.path.join('app', 'static', 'uploads')
    return send_from_directory(upload_folder, filename, as_attachment=True)

@bp.route('/view_assignment/<int:assignment_id>', methods=['GET'])
@login_required
def view_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = Submission.query.filter_by(assignment_id=assignment.id).all()

    # Calculate the deadline time
    deadline_time = assignment.created_on + timedelta(minutes=assignment.deadline_duration)

    # Update overdue status for each submission
    for submission in submissions:
        if submission.status == 'pending' and datetime.utcnow() > deadline_time:
            submission.status = 'overdue'
            db.session.commit()

    return render_template('lecturer/view_assignment.html', assignment=assignment, submissions=submissions)

@bp.route('/courses', methods=['GET', 'POST'])
@login_required
def manage_courses():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            description=form.description.data,
            lecturer_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        flash('Khóa học đã được tạo thành công!')
        return redirect(url_for('lecturer.manage_courses'))

    courses = Course.query.filter_by(lecturer_id=current_user.id).all()
    return render_template('lecturer/manage_courses.html', form=form, courses=courses)

@bp.route('/course/<int:course_id>/videos', methods=['GET', 'POST'])
@login_required
def manage_videos(course_id):
    course = Course.query.get_or_404(course_id)
    if course.lecturer_id != current_user.id:
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    form = UploadVideoForm()
    if form.validate_on_submit():
        video_file = form.video.data
        video_path = os.path.join('app', 'static', 'videos', secure_filename(video_file.filename))
        video_file.save(video_path)
        video_url = f"videos/{secure_filename(video_file.filename)}"

        video = LectureVideo(
            title=form.title.data,
            video_url=video_url,
            course_id=course.id
        )
        db.session.add(video)
        db.session.commit()
        flash('Video đã được tải lên thành công!')
        return redirect(url_for('lecturer.manage_videos', course_id=course.id))

    videos = LectureVideo.query.filter_by(course_id=course.id).all()
    return render_template('lecturer/manage_videos.html', form=form, course=course, videos=videos)

@bp.route('/class/manage/<int:class_id>', methods=['GET', 'POST'])
@login_required
def manage_class(class_id):
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))
    
    class_ = Class.query.get_or_404(class_id)
    students = [enrollment.student for enrollment in class_.enrollments]

    if request.method == 'POST':
        student_ids = request.form.getlist('students')
        for student_id in student_ids:
            enrollment = Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()
            if enrollment:
                db.session.delete(enrollment)
        db.session.commit()
        flash('Sinh viên đã được xóa khỏi lớp thành công!')
        return redirect(url_for('lecturer.manage_class', class_id=class_id))
    
    return render_template('lecturer/manage_class.html', class_=class_, students=students)
