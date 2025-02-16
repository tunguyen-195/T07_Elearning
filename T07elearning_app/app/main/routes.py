from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import JoinClassForm
from app.models import Class, Enrollment
from app.extensions import db

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('main/index.html', title='Home')

@bp.route('/create_class', methods=['GET', 'POST'])
@login_required
def create_class():
    # Chỉ cho phép lecturer hoặc admin
    if not (current_user.is_lecturer() or current_user.is_admin()):
        flash("Bạn không có quyền tạo phòng học", "danger")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        new_meet = Meeting(
            title=title,
            description=description,
            host_id=current_user.id,
        )
        db.session.add(new_meet)
        db.session.commit()
        flash("Phòng học trực tuyến đã được tạo!", "success")
        return redirect(url_for('main.index'))
    
    return render_template('classroom/create_class.html')

@bp.route('/join_class', methods=['GET', 'POST'])
@login_required
def join_class():
    if request.method == 'POST':
        class_code = request.form.get('class_code')
        class_ = Class.query.filter_by(name=class_code).first()
        if class_:
            enrollment = Enrollment(student_id=current_user.id, class_id=class_.id)
            db.session.add(enrollment)
            db.session.commit()
            flash('You have successfully joined the class!')
            return redirect(url_for('main.index'))
        else:
            flash('Class not found. Please check the class code.')
    return render_template('main/join_class.html')

@bp.route('/room/<meeting_slug>')
@login_required
def room(meeting_slug):
    """
    Màn hình hiển thị phòng học trực tuyến, 
    meeting_slug là duy nhất -> load Meeting tương ứng.
    """
    meet = Meeting.query.filter_by(meeting_slug=meeting_slug).first_or_404()
    return render_template('classroom/classroom.html', meeting=meet)
