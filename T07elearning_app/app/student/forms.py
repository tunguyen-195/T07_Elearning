# app/student/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class SubmitAssignmentForm(FlaskForm):
    file = FileField('Upload Assignment', validators=[DataRequired()])
    submit = SubmitField('Submit')
