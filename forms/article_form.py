from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, HiddenField, widgets, IntegerField
from wtforms.validators import DataRequired, NumberRange
from models import Category


class ArticleForm(FlaskForm):
    # coerce 表示选项值强制转换为int类型
    cate = SelectField("分类：", coerce=int,
                       validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    title = StringField("标题：",
                        validators=[DataRequired()],
                        render_kw={"class": "form-control"})
    thumb = HiddenField("")
    intro = TextAreaField("摘要：",
                          validators=[DataRequired()],
                          render_kw={"class": "form-control"})
    content = TextAreaField("正文：",
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})


class ArticleSearchForm(FlaskForm):
    q = StringField('关键字：',
                    validators=[DataRequired()],
                    render_kw={'class': 'form-control'})
    field = SelectField('查询字段：',
                        choices=[('title', '按照标题查找'), ('content', '按照内容查找')],
                        render_kw={'class': 'form-control'})
    order = SelectField('排序：', choices=[('1', '按照id升序'), ('2', '按照id降序')],
                        render_kw={'class': 'form-control'})


class CategoryForm(FlaskForm):
    name = StringField('分类名称：', validators=[DataRequired('必须输入分类名称')], render_kw={'class': 'form-control'})
    order = IntegerField('显示顺序：',
                         validators=[DataRequired('分类顺序必须是0-20数字'), NumberRange(0, 20, message='分类顺序必须是1-20数字')],
                         default=1,
                         render_kw={'class': 'form-control'})
