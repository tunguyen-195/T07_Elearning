# app/student/routes.py
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from app.student import bp
from app.models import Enrollment, Submission, Assignment, Class, Course, LectureVideo
from app.student.forms import SubmitAssignmentForm
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
def dashboard():
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student/dashboard.html', enrollments=enrollments)

@bp.route('/submit_assignment/<int:assignment_id>', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    submission = Submission.query.filter_by(assignment_id=assignment.id, student_id=current_user.id).first()

    # Calculate the deadline time
    deadline_time = assignment.created_on + timedelta(minutes=assignment.deadline_duration)

    # Check if the submission is late
    if datetime.utcnow() > deadline_time:
        flash('The deadline for this assignment has passed.', 'danger')
        return redirect(url_for('student.view_assignment', assignment_id=assignment.id))

    # Check if the submission exists and is not pending
    if submission and submission.status != 'pending':
        flash('Bạn đã nộp bài tập này rồi.', 'danger')
        return redirect(url_for('student.view_assignment', assignment_id=assignment.id))

    if 'file' not in request.files or request.files['file'].filename == '':
        flash('Không có file nào được tải lên.', 'danger')
        return redirect(url_for('student.view_assignment', assignment_id=assignment.id))

    file = request.files['file']
    answer = request.form.get('answer', '')

    # Save file
    upload_folder = os.path.join('app', 'static', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join('uploads', secure_filename(file.filename)).replace('\\', '/')  # Ensure forward slashes
    full_file_path = os.path.join(upload_folder, secure_filename(file.filename))
    file.save(full_file_path)

    # If submission exists and is pending, update it
    if submission and submission.status == 'pending':
        submission.file_url = file_path
        submission.answer = answer
        submission.submission_date = datetime.utcnow()
        submission.status = 'submitted'
    else:
        # Create a new submission
        submission = Submission(
            assignment_id=assignment.id,
            student_id=current_user.id,
            submission_date=datetime.utcnow(),
            file_url=file_path,  # Store relative path with forward slashes
            status='submitted',
            feedback='',  # Initialize feedback as empty
            grade=None,  # Initialize grade as None
            answer=answer  # Save the answer text
        )
        db.session.add(submission)

    db.session.commit()

    flash('Bài tập của bạn đã được nộp!', 'success')
    return redirect(url_for('student.view_assignment', assignment_id=assignment.id))

@bp.route('/view_assignments')
@login_required
def view_assignments():
    if not current_user.is_student():  # Check if the user is a student
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('main.index'))  # Redirect to main page

    submissions = Submission.query.filter_by(student_id=current_user.id).all()
    return render_template('student/assignments.html', submissions=submissions)

@bp.route('/create_assignment', methods=['GET', 'POST'])
@login_required
def create_assignment():
    if request.method == 'POST':
        title = request.form['title']
        class_id = request.form['class_id']
        attachment = request.files.get('attachment')  # Lấy file đính kèm

        new_assignment = Assignment(title=title, class_id=class_id)

        if attachment:
            attachment_path = os.path.join('app', 'static', 'uploads', secure_filename(attachment.filename))
            attachment.save(attachment_path)
            new_assignment.attachment_url = attachment_path  # Lưu đường dẫn file vào model

        db.session.add(new_assignment)
        db.session.commit()

        flash('Assignment created successfully! You can manage your assignments now.', 'success')
        return redirect(url_for('student.manage_assignments'))  # Redirect to the management page

    classes = Class.query.all()  # Fetch classes for the form
    return render_template('student/create_assignment.html', classes=classes)

@bp.route('/manage_assignments')
@login_required
def manage_assignments():
    if not current_user.is_lecturer():  # Check if the user is a lecturer
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('student.view_assignments'))  # Redirect to student view assignments

    assignments = Assignment.query.all()  # Fetch all assignments
    return render_template('student/manage_assignments.html', assignments=assignments)

@bp.route('/assignment/<int:assignment_id>', methods=['GET'])
@login_required
def view_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    submission = Submission.query.filter_by(assignment_id=assignment.id, student_id=current_user.id).first()

    # Calculate the deadline time
    deadline_time = assignment.created_on + timedelta(minutes=assignment.deadline_duration)
    remaining_time = (deadline_time - datetime.utcnow()).total_seconds()

    # Check if the submission is overdue
    if remaining_time <= 0 and (not submission or submission.status == 'pending'):
        if submission:
            submission.status = 'overdue'
        else:
            submission = Submission(
                assignment_id=assignment.id,
                student_id=current_user.id,
                submission_date=None,
                file_url=None,
                status='overdue',
                feedback='',
                grade=None,
                answer=''
            )
            db.session.add(submission)
        db.session.commit()

    return render_template('student/view_assignment.html', assignment=assignment, submission=submission, remaining_time=remaining_time)

@bp.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('static/uploads', filename, as_attachment=True)

@bp.route('/courses', methods=['GET'])
@login_required
def view_courses():
    if not current_user.is_student():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    courses = Course.query.all()
    return render_template('student/view_courses.html', courses=courses)

@bp.route('/course/<int:course_id>/videos', methods=['GET'])
@login_required
def view_videos(course_id):
    if not current_user.is_student():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    course = Course.query.get_or_404(course_id)
    videos = LectureVideo.query.filter_by(course_id=course.id).all()
    return render_template('student/view_videos.html', course=course, videos=videos)
