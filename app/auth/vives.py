from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegisterForm, EditUserinfoForm, ChangePasswordForm
from .. import db
from ..models import UserTable


@auth.route("/", methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()
        if user is not None and user.is_lock == True:
            flash("账户已锁定，无法登陆")
            return redirect(url_for('auth.login'))
        elif user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get("next") or url_for('main.index'))
        else:
            flash("登陆失败")
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("已退出登录")
    return redirect(url_for('auth.login'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = UserTable(username=form.username.data,
                         password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_info(username):
    userobj = UserTable.query.filter_by(username=username, user_id=current_user.get_id()).first_or_404()
    return render_template('auth/user_info.html', userobj=userobj)


@auth.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    form = EditUserinfoForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.real_name.data != '':
            current_user.real_name = form.real_name.data
        if form.phone_number.data != '':
            current_user.phone_number = form.phone_number.data
        if form.sex.data != '':
            current_user.sex = form.sex.data
        if form.address.data != '':
            current_user.address = form.address.data
        if form.about_me.data != '':
            current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()

        return redirect(url_for('auth.user_info', username=current_user.username))
    return render_template('auth/setting.html', form=form)


@auth.route('/change_pass/', methods=['GET', 'POST'])
@login_required
def change_pass():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('auth.user_info', username=current_user.username))
        else:
            flash('密码验证错误')
            return redirect(url_for('auth.change_pass'))
    return render_template("auth/change_pass.html", form=form)
