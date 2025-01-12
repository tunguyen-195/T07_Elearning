# app/lecturer/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired

class CreateCourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Course')

class CreateAssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    max_attempts = IntegerField('Max Attempts', validators=[DataRequired()])
    submit = SubmitField('Create Assignment')
