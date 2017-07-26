from flask_wtf import FlaskForm as Form
from wtforms import StringField,  validators,SubmitField


class share_pass(Form):
    password=StringField('访问密码',[validators.Length(min=4, max=4, message="密码为四位数字")])
    submit = SubmitField('提交')