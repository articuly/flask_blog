from flask import request, redirect, url_for, render_template, jsonify
from libs import db, csrf
from models import User
from .admin_app import admin_app
import json
from forms.account_form import AdminEditInfoForm, UserSearch


# 如果用户刚进入列表页是访问http://127.0.0.1/user/list与"/list/<int:page>"不匹配，提供一个默认带有page默认值的路由
# 用户列表功能，用get方法修复搜索后按2之后分页会回到全用户搜索的问题
@admin_app.route('/user/list/', methods=['get', 'post'])
def userList():
    form = UserSearch()
    q = request.args.get('q')
    page = request.args.get('page', 1)
    if q is not None:
        page = request.args.get('page', 1)
        form_field = request.args.get('field')
        form_sex = request.args.get('sex')
        form_order = request.args.get('order')
        print(q, form_field, form_sex, form_order)
        # condition = {request.form['field']: q}
        # filter_by
        # users = User.query.filter_by(**condition).all()
        # filter like
        if form_field == 'username':
            condition = User.username.like('%%%s%%' % q)
        else:
            condition = User.realname.like('%%%s%%' % q)
        if form_order == '1':
            order = User.id.asc()
        else:
            order = User.id.desc()
        if request.args.get('sex') == '0':
            res = User.query.filter(condition).order_by(order).paginate(int(page), 10)
        else:
            res = User.query.filter(condition, User.sex == request.args.get('sex')).order_by(order).paginate(page, 10)
        users = res.items
        pageList = res.iter_pages()
        total = res.total
        pages = res.pages
        # 有条件搜索和无搜索转到同一模板，用模板语法来区分get的链接
        return render_template('admin/user/user_list.html', users=users, pageList=pageList, pages=pages, total=total,
                               form=form, q=q, field=form_field, sex=form_sex, order=form_order)
    else:
        # users = User.query.all()
        # 无论搜索还是默认查看，都是翻页处理
        res = User.query.paginate(int(page), 10)
        users = res.items
        pageList = res.iter_pages()
        total = res.total
        pages = res.pages
        print(q, total)
        # 有条件搜索和无搜索转到同一模板，用模板语法来区分get的链接
        return render_template('admin/user/user_list.html', users=users, pageList=pageList, pages=pages, total=total,
                               form=form, q=q)


# 根据用户id删除用户，启用csrf保护
@admin_app.route('/user/delete/', methods=['post'])
def deleteUser():
    csrf.protect()
    user_id = int(request.form.get('user_id'))
    print('调用csrf后删除用户', user_id)
    message = {}
    if user_id != 1:  # 防止admin被删除
        user = User.query.get(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            message['result'] = 'fail'
        else:
            message['result'] = 'success'
    else:
        message['result'] = '不能删除管理员账号'
    return json.dumps(message)


# 修改所有用户信息
@admin_app.route("/user/edit/<int:user_id>", methods=['get', 'post'])
def editUser(user_id):
    form = AdminEditInfoForm()
    user = User.query.get_or_404(user_id)
    print('form data is in')
    if form.validate_on_submit():
        message = {'result': 'fail'}
        user.realname = form.data['name']
        user.sex = form.data['sex']
        user.hobby = ', '.join(form.data['hobby'])
        user.city = form.data['city']
        user.intro = form.data['intro']
        try:
            db.session.commit()
            print('准备提交')
        except Exception as e:
            print(str(e))
        else:
            message['result'] = 'success'
        return jsonify(message)
    elif form.errors:
        print(form.errors)
    else:
        form.name.data = user.realname
        form.sex.data = user.sex
        form.hobby.data = user.hobby.split(', ')
        form.city.data = user.city
        form.intro.data = user.intro
    return render_template("admin/user/user_edit.html", user_id=user_id, form=form)
