# app/lecturer/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, DateTimeField, SelectField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, ValidationError
from app.models import Class, Enrollment, Assignment, Submission, User
import re
from datetime import datetime
def validate_url(form, field):
    url = field.data
    if not re.match(r'^(http|https)://', url):
        url = 'http://' + url  # Add default scheme
    field.data = url  # Update the field data with the complete URL
    # Validate the URL format
    if not re.match(r'^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$', url):
        raise ValidationError('Invalid URL format.')

class CreateAssignmentForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    due_date = DateTimeField('Hạn nộp', format='%Y-%m-%d', validators=[DataRequired()])
    class_id = SelectField('Lớp', coerce=int, validators=[DataRequired()])
    attachment = FileField('Tệp đính kèm')
    deadline_duration = IntegerField('Deadline Duration (minutes)', validators=[DataRequired()])
    class_link = StringField('Link Phòng Học', validators=[Optional(), validate_url])
    submit = SubmitField('Tạo Bài Tập')

    def __init__(self, *args, **kwargs):
        super(CreateAssignmentForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(cls.id, cls.name) for cls in Class.query.all()]

def validate_due_date(form, field):
    if field.data < datetime.utcnow():
        raise ValidationError("Due date must be in the future.")

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    due_date = DateTimeField('Due Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired(), validate_due_date])
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Assignment')
    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(cls.id, cls.name) for cls in Class.query.all()]

class CreateClassForm(FlaskForm):
    name = StringField('Tên Lớp', validators=[DataRequired()])
    description = TextAreaField('Mô Tả')
    submit = SubmitField('Tạo Lớp')

class EnrollStudentsForm(FlaskForm):
    excel_file = FileField('Tải lên Danh sách lớp - Excel', validators=[Optional()])  # Không bắt buộc
    submit = SubmitField('Thêm Sinh Viên')


class CreateCourseForm(FlaskForm):
    name = StringField('Tên Khóa Học', validators=[DataRequired()])
    description = TextAreaField('Mô Tả')
    classes = SelectMultipleField('Chọn Lớp', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Tạo Khóa Học')

    def __init__(self, *args, **kwargs):
        super(CreateCourseForm, self).__init__(*args, **kwargs)
        self.classes.choices = [(cls.id, cls.name) for cls in Class.query.all()]

class UploadVideoForm(FlaskForm):
    title = StringField('Tên Video', validators=[DataRequired()])
    video = FileField('Tệp Video', validators=[DataRequired()])
    submit = SubmitField('Tải Lên Video')

