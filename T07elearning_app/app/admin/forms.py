# app/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.models import Role

class AssignRoleForm(FlaskForm):
    user = SelectField('User', coerce=int, validators=[DataRequired()])
    role = SelectField('Role', choices=[], validators=[DataRequired()])
    submit = SubmitField('Assign Role')

    def __init__(self, *args, **kwargs):
        super(AssignRoleForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.all()]
        self.user.choices = [(user.id, user.username) for user in Role.query.filter_by(name='student').first().users]
