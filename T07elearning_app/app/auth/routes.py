# app/auth/routes.py
import logging
from flask import render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import bp
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordForm, ChangePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

# app/auth/routes.py
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        app.logger.debug("Form đã được xác thực.")
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        app.logger.debug("Người dùng đã đăng nhập thành công.")
        flash('Đăng nhập thành công!', 'success')
        return redirect(url_for('main.index'))
    else:
        if request.method == 'POST':
            flash('Form validation failed.', 'danger')
            app.logger.debug("Xác thực form thất bại.")
            app.logger.debug(f"Form Errors: {form.errors}")  # Thêm dòng này để log lỗi
    return render_template('auth/login.html', form=form)

@bp.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.', 'danger')
            return redirect(url_for('auth.register'))
        new_user = User(
            username=form.username.data,
            fullname=form.fullname.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)  # Sửa ở đây

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # TODO: Gửi email khôi phục mật khẩu cho người dùng
            flash('Một email khôi phục mật khẩu đã được gửi đến địa chỉ email của bạn.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Tên đăng nhập không tồn tại.', 'danger')
    return render_template('auth/reset_password.html', form=form)  # Sửa ở đây

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('auth/signup.html')  # Đảm bảo template này tồn tại

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Mật khẩu của bạn đã được thay đổi thành công!', 'success')
        return redirect(url_for('main.index'))
    else:
        if request.method == 'POST':
            flash('Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.', 'danger')
    return render_template('auth/change_password.html', form=form)
