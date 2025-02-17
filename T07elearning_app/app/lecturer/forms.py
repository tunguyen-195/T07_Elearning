# app/lecturer/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, DateTimeField, SelectField, FileField
from wtforms.validators import DataRequired
from app.models import Class, Enrollment, Assignment, Submission, User

class CreateAssignmentForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    description = TextAreaField('Mô tả')
    due_date = DateTimeField('Hạn nộp', format='%Y-%m-%d', validators=[DataRequired()])
    class_id = SelectField('Lớp', coerce=int, validators=[DataRequired()])
    attachment = FileField('Tệp đính kèm')
    submit = SubmitField('Tạo Bài Tập')

    def __init__(self, *args, **kwargs):
        super(CreateAssignmentForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(cls.id, cls.name) for cls in Class.query.all()]

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    due_date = DateTimeField('Due Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
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
    submit = SubmitField('Thêm Sinh Viên')

