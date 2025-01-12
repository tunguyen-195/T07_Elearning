# app/lecturer/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.lecturer import bp
from app.models import Course, Assignment
from app.lecturer.forms import CreateCourseForm, CreateAssignmentForm
from app.extensions import db

@bp.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    if not current_user.is_lecturer():
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    form = CreateCourseForm()
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            description=form.description.data,
            lecturer_id=current_user.id,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Course has been created!')
        return redirect(url_for('lecturer.dashboard'))
    return render_template('lecturer/create_course.html', form=form)

@bp.route('/create_assignment/<int:course_id>', methods=['GET', 'POST'])
@login_required
def create_assignment(course_id):
    if not current_user.is_lecturer():
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    form = CreateAssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            course_id=course_id,
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            max_attempts=form.max_attempts.data
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment has been created!')
        return redirect(url_for('lecturer.course_detail', course_id=course_id))
    return render_template('lecturer/create_assignment.html', form=form)
