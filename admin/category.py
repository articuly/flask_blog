from flask import request, session, render_template, redirect, url_for
from .admin_app import admin_app
from models import Article, Category
from libs import db
from forms.article_form import CategoryForm


# 添加分类
@admin_app.route('/category/add_cate', methods=['get', 'post'])
def addCate():
    message = None
    form = CategoryForm()
    if form.validate_on_submit():
        cate_name = form.data['name']
        cate_order = form.data['order']
        category = Category(
            cate_name=cate_name,
            cate_order=cate_order,
        )
        try:
            db.session.add(category)
            db.session.commit()
            message = cate_name + '分类添加成功'
        except Exception as e:
            message = '发生了错误：' + str(e)
            # 如果插入失败，进行回滚操作
            db.session.rollback()
    else:
        print(form.errors)
    return render_template('admin/category/category_add.html', message=message, form=form)


# 获得分类列表
@admin_app.route('/category/cate_list/<int:page>', methods=['get'])
@admin_app.route('/category/cate_list', defaults={'page': 1}, methods=['get'])
def cateList(page):
    res = Category.query.order_by(Category.cate_order).paginate(page, 10)
    cates = res.items
    pageList = res.iter_pages()
    return render_template('admin/category/category_list.html', cates=cates, pageList=pageList)


# 删除分类
@admin_app.route('/category/cate_delete/<int:cate_id>')
def deleteCate(cate_id):
    cate = Category.query.get(cate_id)
    db.session.delete(cate)
    db.session.commit()
    return redirect(url_for('.cateList'))


# 修改分类
@admin_app.route('/category/cate_edit/<int:cate_id>', methods=['get', 'post'])
def editCate(cate_id):
    form = CategoryForm()
    category = Category.query.get(cate_id)
    if form.validate_on_submit():
        category.cate_name = form.data['name']
        category.cate_order = form.data['order']
        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
        else:
            return redirect(url_for(".cateList"))
    elif form.errors:
        print(form.errors)
    else:
        form.name.data = category.cate_name
        form.order.data = category.cate_order
    return render_template('admin/category/category_edit.html', form=form, category=category)
