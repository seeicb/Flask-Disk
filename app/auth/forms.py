from flask_wtf import FlaskForm as Form
from flask import session
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, ValidationError, SelectField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, Length
from ..models import UserTable


class LoginForm(Form):
    username = StringField([validators.Length(min=4, max=20, message='用户名必须在4-20个字符串之间')])
    password = PasswordField([validators.Length(min=4, max=32)])
    verification_code = StringField('验证码: ', validators=[DataRequired(), Length(4, 4, message='填写4位验证码')])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')

    def validate_verification_code(self, fiels):
        if session['captcha'].lower() != fiels.data.lower():
            print(session['captcha'], fiels.data)
            raise ValidationError('验证码错误')


class RegisterForm(Form):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(
        4, 20, message='用户名必须在4-20个字符串之间'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message='用户名必须由字母数、字数、下划线或 . 组成')])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message='密码必须由字母数、字数、下划线或 . 组成'),
        EqualTo('password_confirm', message='密码必须一至')])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(message='密码不能为空')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Length(1, 100), Email(message='邮箱格式不正确')])
    # verification_code = StringField('验证码: ', validators=[DataRequired(), Length(4, 4, message='填写4位验证码')])
    submit = SubmitField('注册')

    def validate_username(self, field):
        if UserTable.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')

    def validate_email(self, field):
        if UserTable.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    # def validate_verification_code(self, fiels):
    #     if session['captcha'].lower() != fiels.data.lower():
    #         print(session['captcha'], fiels.data)
    #         raise ValidationError('验证码错误')


class ChangePasswordForm(Form):
    old_password = PasswordField('原密码', [validators.Length(min=4, max=32)])
    new_password = PasswordField('新的密码', validators=[
        DataRequired(message='密码不能为空'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message='密码必须由字母数、字数、下划线或 . 组成'),
        EqualTo('password_confirm', message='密码必须一至')])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(message='密码不能为空')])
    submit = SubmitField('提交')


class EditUserinfoForm(Form):
    real_name = StringField('姓名', validators=[Length(0, 64)])
    phone_number = StringField('手机号码', validators=[Length(0, 20)])
    sex = SelectField('性别', choices=[('男', '男'), ('女', '女')], validators=[Length(0, 64)])
    address = StringField('地址', validators=[Length(0, 100)])
    about_me = TextAreaField('自我简介')
    submit = SubmitField('提交')
