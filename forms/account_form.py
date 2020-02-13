from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, SelectField, RadioField, \
    TextAreaField, widgets


class CheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    # widget = widgets.ListWidget()
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField('用户名', render_kw={'class': 'form-control', 'placeholder': 'enter your name'})
    password = PasswordField('密码', render_kw={'class': 'form-control', 'placeholder': 'enter your password'})
    # 多选框选项
    choices = [(1, '一周免登录'), (2, '两周免登录'), (3, '三周免登录')]
    remember = CheckBoxField('记住登录', choices=choices)
    submit = SubmitField('', render_kw={'class': 'btn btn-default', 'value': 'Login'})
