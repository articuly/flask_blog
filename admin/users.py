from flask import request, redirect, url_for, render_template
from libs import db
from models import User
from .admin_app import admin_app
import json


# 用户注册功能
# TODO change position
@admin_app.route('/register', methods=['get', 'post'])
def register():
    message = None
    if request.method == 'POST':
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
    return render_template('user/register.html', message=message)


# 验证是否存在同名用户
def validate_username(username):
    return User.query.filter_by(username=username).first()


# 如果用户刚进入列表页是访问http://127.0.0.1/user/list与"/list/<int:page>"不匹配，提供一个默认带有page默认值的路由
# 用户列表功能
@admin_app.route('/user/list/<int:page>', methods=['get', 'post'])
@admin_app.route('/user/list', defaults={'page': 1}, methods=['get', 'post'])
def userList(page):
    if request.method == 'POST':
        q = request.form['q']
        condition = {request.form['field']: q}
        # filter_by
        # users = User.query.filter_by(**condition).all()
        # filter like
        if request.form['field'] == 'realname':
            condition = User.realname.like('%%%s%%' % q)
        else:
            condition = User.username.like('%%%s%%' % q)
        if request.form['order'] == '1':
            order = User.id.asc()
        else:
            order = User.id.desc()
        if request.form['sex'] == '':
            res = User.query.filter(condition).order_by(order).paginate(page, 10)
        else:
            res = User.query.filter(condition, User.sex == request.form['sex']).order_by(order).paginate(page, 10)
    else:
        # users = User.query.all()
        # 无论搜索还是默认查看，都是翻页处理
        res = User.query.paginate(page, 10)
    users = res.items
    pageList = res.iter_pages()
    total = res.total
    pages = res.pages
    return render_template('admin/user/user_list.html', users=users, pageList=pageList, pages=pages, total=total)


# 根据用户id删除用户
@admin_app.route('/user/delete/<int:user_id>')
def deleteUser(user_id):
    if user_id != 1:  # 防止admin被删除
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for(".userList"))
    else:
        return redirect(url_for(".userList"))


# 用户信息修改
@admin_app.route("/user/edit/<int:user_id>", methods=['get', 'post'])
def editUser(user_id):
    user = User.query.get(user_id)
    if request.method == "POST":
        user.username = request.form['username']
        user.realname = request.form['name']
        user.sex = request.form['sex']
        user.hobby = ', '.join(request.form.getlist('hobby'))
        user.city = request.form['city']
        user.intro = request.form['intro']
        db.session.commit()
        return redirect(url_for(".userList"))
    return render_template("admin/user/user_edit.html", user=user)
