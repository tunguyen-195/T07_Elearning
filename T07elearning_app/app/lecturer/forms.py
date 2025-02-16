# app/lecturer/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, DateTimeField, SelectField, FileField
from wtforms.validators import DataRequired
from app.models import Class

class CreateCourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Course')

class CreateAssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateTimeField('Due Date', format='%Y-%m-%d %H:%M:%S')
    class_id = SelectField('Class', coerce=int)
    attachment = FileField('Attachment')
    submit = SubmitField('Create Assignment')

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
