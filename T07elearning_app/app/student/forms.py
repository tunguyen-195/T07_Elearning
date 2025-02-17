# app/student/forms.py
from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SubmitAssignmentForm(FlaskForm):
    file = FileField('Tệp đính kèm')
    answer = TextAreaField('Câu trả lời', validators=[DataRequired()])
    submit = SubmitField('Nộp Bài Tập')
