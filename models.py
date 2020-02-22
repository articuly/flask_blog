from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 用户数据库
class User(db.Model):
    # 数据库字段映射到Python的变量
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    city = db.Column(db.String)
    hobby = db.Column(db.String)
    intro = db.Column(db.String)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


# 文章数据库
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    thumb = db.Column(db.String)
    intro = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.Text)
    pubdate = db.Column(db.DateTime, default=datetime.now)
    cate_id = db.Column(db.Integer, db.ForeignKey('category.cate_id'))


# 目录数据库，是文章的从表
class Category(db.Model):
    cate_id = db.Column(db.Integer, primary_key=True)
    # unique=True,表示此字段值不能重复
    cate_name = db.Column(db.String, unique=True)
    cate_order = db.Column(db.Integer, default=0)
    articles = db.relationship('Article')

# class Alert(db.Model):
#     pass
