from flask import request, session, render_template, redirect, url_for
from .admin_app import admin_app
from models import Article, Category
from libs import db


# 根据文章cate_id显示文章列表
# TODO change position
@admin_app.route('/cate/<int:cate_id>/<int:page>')
@admin_app.route('/', defaults={'cate_id': 0, 'page': 1})
def getArticleList(cate_id, page):
    if cate_id == 0:
        res = Article.query.paginate(page, 15)
    else:
        res = Article.query.filter_by(cate_id=cate_id).paginate(page, 15)
    category = Category.query.get(cate_id)
    articles = res.items
    pageList = res.iter_pages()
    return render_template('cate_articles.html', cate_id=cate_id, articles=articles, pageList=pageList,
                           category=category)


# 添加分类
@admin_app.route('/category/add_cate', methods=['get', 'post'])
def addCate():
    message = None
    if request.method == 'POST':
        cate_name = request.form['name']
        cate_order = request.form['order']
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
    return render_template('admin/category/category_add.html', message=message)


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
    category = Category.query.get(cate_id)
    if request.method == 'POST':
        category.cate_name = request.form['name']
        category.cate_order = request.form['order']
        db.session.commit()
        return redirect(url_for(".cateList"))
    return render_template('admin/category/category_edit.html', category=category)
