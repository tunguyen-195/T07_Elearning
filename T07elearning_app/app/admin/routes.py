# app/admin/routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, Role
from app.admin.forms import AssignRoleForm
from app.extensions import db

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@bp.route('/assign_role', methods=['GET', 'POST'])
@login_required
def assign_role():
    if not current_user.is_admin():
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    form = AssignRoleForm()
    if form.validate_on_submit():
        user = User.query.get(form.user.data)
        role = Role.query.get(form.role.data)
        if role not in user.roles:
            user.roles.append(role)
            db.session.commit()
            flash('Role has been assigned!')
        else:
            flash('User already has this role.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/assign_role.html', form=form)
