# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Regexp
from app.models import User
from flask_login import current_user
from werkzeug.security import check_password_hash

class LoginForm(FlaskForm):
    username = StringField('Tên Đăng Nhập', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=3)])
    remember_me = BooleanField('Ghi nhớ tôi')
    submit = SubmitField('Đăng nhập')

class RegisterForm(FlaskForm):
    username = StringField('Tên Đăng Nhập', validators=[DataRequired(), Length(min=2, max=50)])
    fullname = StringField('Họ và Tên', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Đăng ký')

class ResetPasswordForm(FlaskForm):
    username = StringField('Tên Đăng Nhập', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Khôi phục mật khẩu')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Tên đăng nhập không tồn tại. Vui lòng kiểm tra lại.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mật khẩu hiện tại', validators=[DataRequired()])
    new_password = PasswordField('Mật khẩu mới', validators=[
        DataRequired(),
        Length(min=8, message='Mật khẩu phải có ít nhất 8 ký tự.'),
        Regexp(r'(?=.*[!@#$%^&*])', message='Mật khẩu phải chứa ít nhất một ký tự đặc biệt.')
    ])
    confirm_new_password = PasswordField('Xác nhận mật khẩu mới', validators=[
        DataRequired(),
        EqualTo('new_password', message='Mật khẩu xác nhận không khớp.')
    ])
    submit = SubmitField('Đổi mật khẩu')

    def validate_current_password(self, field):
        if not check_password_hash(current_user.password_hash, field.data):
            raise ValidationError('Mật khẩu hiện tại không đúng.')
