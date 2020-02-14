from flask import request, redirect, url_for, render_template
from libs import db
from models import User
from flask import Blueprint
from forms.account_form import RegisterForm

user_app = Blueprint("user_app", __name__)


# 用户注册功能
@user_app.route('/register', methods=['get', 'post'])
def register():
    message = None
    form = RegisterForm()
    if form.validate_on_submit():
        if validate_username(request.form['username']):
            return render_template('user/register.html', message='用户名重复')
        realname = request.form['name']
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']
        hobby = ', '.join(request.form.getlist('hobby'))
        city = request.form['city']
        intro = request.form['intro']
        user = User(
            realname=realname,
            username=username,
            password=password,
            sex=sex,
            hobby=hobby,
            city=city,
            intro=intro,
        )
        # 密码加码
        user.hash_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            message = '注册失败' + str(e)
    else:
        print(form.errors)
    return render_template('user/register.html', message=message, form=form)


# 验证是否存在同名用户
def validate_username(username):
    return User.query.filter_by(username=username).first()
