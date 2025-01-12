from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import JoinClassForm

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
def join_class():
    """
    Xử lý logic để người dùng nhập MeetingSlug -> redirect sang /room/<meeting_slug>
    """
    form = JoinClassForm()
    if form.validate_on_submit():
        meeting_id_input = form.meeting_id.data.strip()
        # Tìm meeting dựa trên meeting_slug
        room = Meeting.query.filter_by(meeting_slug=meeting_id_input).first()

        if not room:
            flash(f"Không tìm thấy phòng với ID/Slug: {meeting_id_input}", "danger")
            return redirect(url_for('main.join_class'))
        
        # Khi tìm thấy, chuyển hướng sang route 'main.room'
        return redirect(url_for('main.room', meeting_slug=room.meeting_slug))
    
    return render_template('main/join_class.html', form=form)

@bp.route('/room/<meeting_slug>')
@login_required
def room(meeting_slug):
    """
    Màn hình hiển thị phòng học trực tuyến, 
    meeting_slug là duy nhất -> load Meeting tương ứng.
    """
    meet = Meeting.query.filter_by(meeting_slug=meeting_slug).first_or_404()
    return render_template('classroom/classroom.html', meeting=meet)
