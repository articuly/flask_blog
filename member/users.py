from flask import request, redirect, url_for, render_template, session
from libs import db
from models import User
from .member_app import member_app


# 用户信息修改
@member_app.route("/user/edit/", methods=['get', 'post'])
def userEdit():
    # 普通会员只能修改自己的资料
    # TODO 修改资料的时候还需要验证密码
    user = User.query.filter_by(username=session['user']).one()
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.hobby = ', '.join(request.form.getlist('hobby'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for(".userList"))
    return render_template("member/info/info_edit.html", user=user)
