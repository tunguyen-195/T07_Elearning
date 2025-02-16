# app/lecturer/routes.py
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.lecturer import bp
from app.models import Course, Assignment, Class, Enrollment, User
from app.lecturer.forms import CreateCourseForm, CreateAssignmentForm, AssignmentForm, CreateClassForm, EnrollStudentsForm
from app.extensions import db
import os
from werkzeug.utils import secure_filename

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
def create_course_assignment(course_id):
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

@bp.route('/assignment/create', methods=['GET', 'POST'])
@login_required
def create_assignment():
    if not current_user.is_lecturer():
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    
    form = CreateAssignmentForm()
    if form.validate_on_submit():
        # Handle file upload
        file = form.attachment.data
        filename = secure_filename(file.filename)
        file_path = os.path.join('app', 'static', 'uploads', filename)
        file.save(file_path)

        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            class_id=form.class_id.data,
            attachment_url=file_path  # Save the file path
        )
        db.session.add(assignment)
        db.session.commit()
        flash('Assignment created successfully!')
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
