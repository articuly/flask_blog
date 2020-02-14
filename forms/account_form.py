from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, SelectField, RadioField, \
    TextAreaField, widgets
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo


class CheckBoxField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    # widget = widgets.ListWidget()
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    username = StringField('用户名', render_kw={'class': 'form-control', 'placeholder': 'enter your name'},
                           validators=[DataRequired('必须填写用户名'),
                                       Length(6, 20, message='用户名长度在6-20位之间')])
    password = PasswordField('密码', render_kw={'class': 'form-control', 'placeholder': 'enter your password'},
                             validators=[DataRequired('必须填写密码'),
                                         Length(6, 20, message='密码长度在6-20位之间')])
    # # 多选框选项
    # choices = [(1, '一周免登录'), (2, '两周免登录'), (3, '三周免登录')]
    # remember = CheckBoxField('记住登录', choices=choices)
    submit = SubmitField('', render_kw={'class': 'btn btn-default', 'value': '登陆'})


# 如果要定义一个数值区间的验证器，那么参数就类似：
# def __init__(self, min, max, message)
class BadWords:
    def __init__(self, bad_words, message=None):
        '''
        :param bad_words: 敏感词列表
        :param message: 错误提示
        '''
        self.bad_words = bad_words
        if not message:
            message = '不能包含敏感词'
        self.message = message

    def __call__(self, form, field):
        '''
        __call__方法可以让实例对象可以像函数一样调用
        badwords = BadWords(['admin','kf'], message="敏感了")
        验证调用是通过实例调用: badwords(form, field)，
        好像执行了 badwords.__call__(form，field)方法一样
        :param form: 验证表单对象
        :param field: 验证字段对象
        :return:
        '''
        print('自定义验证器调用')
        for word in self.bad_words:
            if field.data.find(word) != -1:
                raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    name = StringField('姓名：',
                       validators=[DataRequired('真实姓名必填'), BadWords(['admin', 'articuly', '客户服务'], message='不能包括敏感词')],
                       render_kw={'class': 'form-control', 'placeholder': "请填写您的真实姓名"})
    username = StringField('用户名：',
                           validators=[DataRequired('用户名必填'),
                                       BadWords(['admin', 'articuly', '客户服务'], message='不能包括敏感词')],
                           render_kw={'class': 'form-control', 'placeholder': '请填写您的用户名，至少6个字符'})
    password = PasswordField('密码：', validators=[DataRequired(message='必须提供密码'), Length(6, 20, message='密码长度在6-20位之间')],
                             render_kw={'class': 'form-control', 'placeholder': "设置一个密码，至少6个字符"})
    confirmpassword = PasswordField('确认密码：', validators=[EqualTo('password', message='两次输入密码不一样')],
                                    render_kw={'class': 'form-control', 'placeholder': "请确认您的密码"})
    sex = RadioField('性别：', validators=[DataRequired('必须选择性别')],
                     choices=[(1, '男'), (2, '女')])
    hobby = CheckBoxField('爱好：', choices=[('travel', '旅行'), ('reading', '阅读'), ('singing', '唱歌'), ('dancing', '跳舞'),
                                          ('writing', '写作'), ('swimming', '游泳'), ('playing basketball', '打篮球')],
                          render_kw={"class": "checkbox-inline"})
    city = SelectField('城市：', validators=[DataRequired('必须所有城市')],
                       choices=[('', '请选择城市'), ('010', '北京'), ('021', '上海'), ('020', '广州'), ('0755', '深圳'),
                                ('0571', '杭州'), ('023', '重庆'), ('0512', '苏州')],
                       render_kw={'class': 'form-control'})
    # 如果这里使用
    # intro = CKEditorField("简介")
    # 输出的textarea中带有class="ckeditor"
    # ckeditor会自动在带有class="ckeditor"的字段上创建富文本编辑器，而不需要
    # 通过{{ ckeditor.config() }}来设置
    intro = TextAreaField('简介:', render_kw={'class': 'form-control'})
    submit = SubmitField('', render_kw={'class': 'btn btn-default', 'value': '立即注册'})

    def validate_username(self, field):
        print('内联验证调用')
        if field.data.find("artic") != -1:
            raise ValidationError("不能包含敏感字")
