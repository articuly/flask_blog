from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for
from functools import wraps
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect

# 创建数据库对象，暂不导入app实例
db = SQLAlchemy()
ckeditor = CKEditor()
csrf = CSRFProtect()


def login_required(func):
    @wraps(func)
    def decorator_nest(*args, **kwargs):
        if not 'user' in session:
            return redirect(url_for('login'))
        else:
            print(func)
            return func(*args, **kwargs)

    return decorator_nest
