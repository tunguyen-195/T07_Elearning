from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url)) 