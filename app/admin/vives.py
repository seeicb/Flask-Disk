from functools import wraps
from flask import render_template, request, flash, jsonify, abort
from flask_login import login_required, current_user
from . import admin
from .forms import changepass_form
from .. import db
from ..models import UserTable


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.get_is_admin():
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/admin/', methods=['GET', 'POST'])
@admin.route('/admin/index/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    userobj = UserTable.query.all()

    return render_template('admin/index.html', userobj=userobj)


@admin.route('/admin/uid/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_detail(id):
    userobj = UserTable.query.filter_by(user_id=id).first_or_404()
    return render_template('admin/user_detail.html', userobj=userobj)


@admin.route('/admin/lock/', methods=['GET', 'POST'])
@login_required
@admin_required
def lock_user():

    if request.method == 'POST':
        id = request.form["id"]
        userobj = UserTable.query.filter_by(user_id=id).first_or_404()
        if userobj.is_admin:
            return render_template('admin/user_detail.html', userobj=userobj)
        userobj.is_lock = True
        db.session.add(userobj)
        db.session.commit()

    return jsonify('success')


@admin.route('/admin/unlock/', methods=['GET', 'POST'])
@login_required
@admin_required
def unlock():
    if request.method == 'POST':
        id = request.form["id"]
        userobj = UserTable.query.filter_by(user_id=id).first_or_404()
        userobj.is_lock = False
        db.session.add(userobj)
        db.session.commit()

    return jsonify('success')


@admin.route('/admin/change_pass/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def change_pass(id):
    form = changepass_form()
    userobj = UserTable.query.filter_by(user_id=id).first_or_404()

    if request.method == 'POST' and form.validate_on_submit():
        userobj.password = form.new_password.data
        db.session.add(userobj)
        db.session.commit()
        flash('密码已经更新')
    return render_template("admin/change_pass.html", form=form, userobj=userobj)