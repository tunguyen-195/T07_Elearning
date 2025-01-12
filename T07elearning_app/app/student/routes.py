# app/student/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.student import bp
from app.models import Enrollment, Course
from app.student.forms import SubmitAssignmentForm
from app.extensions import db

@bp.route('/dashboard')
@login_required
def dashboard():
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student/dashboard.html', enrollments=enrollments)

@bp.route('/submit_assignment/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    form = SubmitAssignmentForm()
    if form.validate_on_submit():
        # Xử lý upload file
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join('app', 'static', 'uploads', filename)
        file.save(file_path)
        submission = Submission(
            assignment_id=assignment_id,
            student_id=current_user.id,
            file_url=file_path,
            status='submitted'
        )
        db.session.add(submission)
        db.session.commit()
        flash('Your assignment has been submitted!')
        return redirect(url_for('student.dashboard'))
    return render_template('student/submit_assignment.html', form=form)
