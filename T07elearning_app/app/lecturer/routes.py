# app/lecturer/routes.py
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from app.lecturer import bp
from app.models import Enrollment, Assignment, Class, User, Submission
from app.lecturer.forms import CreateAssignmentForm, AssignmentForm, CreateClassForm, EnrollStudentsForm
from app.extensions import db
import os
from werkzeug.utils import secure_filename


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
            attachment_url=attachment_url
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
    if request.method == 'POST':
        student_ids = request.form.getlist('students')
        for student_id in student_ids:
            if not Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first():
                enrollment = Enrollment(student_id=student_id, class_id=class_id)
                db.session.add(enrollment)
        db.session.commit()
        flash('Sinh viên đã được thêm vào lớp thành công!')
        return redirect(url_for('lecturer.dashboard'))
    
    return render_template('lecturer/enroll_students.html', class_=class_, students=students, form=form)

@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))
    
    # Query all classes and their students
    classes = Class.query.all()
    class_student_data = []
    for class_ in classes:
        students = [enrollment.student for enrollment in class_.enrollments]
        class_student_data.append({
            'class': class_,
            'students': students
        })
    
    return render_template('lecturer/dashboard.html', class_student_data=class_student_data)

@bp.route('/manage_assignments', methods=['GET'])
@login_required
def manage_assignments():
    if not current_user.is_lecturer():
        flash('Bạn không có quyền truy cập trang này.')
        return redirect(url_for('main.index'))

    assignments = Assignment.query.all()
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
