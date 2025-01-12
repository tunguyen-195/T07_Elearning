# app/main/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class JoinClassForm(FlaskForm):
    meeting_id = StringField('Enter Meeting ID/Slug', validators=[DataRequired()])
    submit = SubmitField('Join')