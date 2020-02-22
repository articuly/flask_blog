from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for
from functools import wraps
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from flask_dropzone import Dropzone

# 创建数据库对象，第三插件的实例，但暂不导入app中
db = SQLAlchemy()
ckeditor = CKEditor()
csrf = CSRFProtect()
dropzone = Dropzone()


# functiools.wraps方式修饰全局的函数，如果没有登陆则跳转到登陆页
def login_required(func):
    @wraps(func)
    def decorator_nest(*args, **kwargs):
        if not 'user' in session:
            return redirect(url_for('login'))
        else:
            print(func)
            return func(*args, **kwargs)

    return decorator_nest
