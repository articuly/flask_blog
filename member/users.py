from flask import request, redirect, url_for, render_template, session
from libs import db
from models import User
from .member_app import member_app
from forms.account_form import EditInfoForm


# 会员修改自己的信息，普通会员只能修改自己的资料
@member_app.route("/user/edit/", methods=['get', 'post'])
def userEdit():
    # TODO 修改资料的时候还需要验证密码
    message = None
    form = EditInfoForm()
    user = User.query.filter_by(username=session['user']).one()
    if form.validate_on_submit():
        user.realname = form.data['name']
        user.sex = form.data['sex']
        user.hobby = ', '.join(form.data['hobby'])
        user.city = form.data['city']
        user.intro = form.data['intro']
        try:
            db.session.commit()
            message = '修改成功'
        except Exception as e:
            print(str(e))
            message = '后台发生错误'
    elif form.errors:
        print(form.errors)
        message = '表单发生错误'
    else:
        form.name.data = user.realname
        form.sex.data = user.sex
        form.hobby.data = user.hobby
        form.city.data = user.city
        form.intro.data = user.intro
    return render_template("member/info/info_edit.html", message=message, user=user, form=form)
