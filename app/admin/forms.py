from flask_wtf import FlaskForm as Form
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Regexp


class changepass_form(Form):
    new_password = PasswordField('新的密码', validators=[
        DataRequired(message='密码不能为空'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message='密码必须由字母数、字数、下划线或 . 组成'),
        EqualTo('password_confirm', message='密码必须一至')])
    password_confirm = PasswordField('确认密码', validators=[DataRequired(message='密码不能为空')])
    submit = SubmitField('提交')
