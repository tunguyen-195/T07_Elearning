# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

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
