from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, HiddenField, widgets
from wtforms.validators import DataRequired
from models import Category

class ArticleForm(FlaskForm):
    # coerce 表示选项值强制转换为int类型
    cate=SelectField("分类", coerce=int,
                     validators=[DataRequired()],
                     render_kw={"class":"form-control"})
    title=StringField("标题",
                      validators=[DataRequired()],
                      render_kw={"class":"form-control"})
    thumb=HiddenField("")
    intro=TextAreaField("摘要",
                        validators=[DataRequired()],
                        render_kw={"class":"form-control"})
    content=TextAreaField("正文",
                          validators=[DataRequired()],
                          render_kw={"class":"form-control"})
