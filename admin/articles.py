from flask import request, redirect, url_for, render_template, session, jsonify
from libs import db, csrf
from models import Article, Category
from .admin_app import admin_app
from forms.article_form import ArticleForm, ArticleSearchForm


# 发布文章
@admin_app.route("/article/post", methods=['get', 'post'])
def article_post():
    form = set_article_form()
    if request.method == "POST":
        # if form.validate_on_submit():
        cate_id = form.data['cate']
        title = form.data['title']
        thumb = form.data['thumb']
        intro = form.data['intro']
        content = form.data['content']
        article = Article(
            cate_id=cate_id,
            title=title,
            thumb=thumb,
            intro=intro,
            content=content,
            author=session['user']
        )
        try:
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            print(str(e))
            message = {'message': '文章发布失败'}
        else:
            message = {'message': '文章发布成功'}
        return jsonify(message)
    return render_template("admin/article/article_post.html", form=form)


# 显示文章列表功能，用get方法修复条件搜索后按2之后的分页跳回全文章列表的问题
@admin_app.route("/article/list/", methods=['get', 'post'])
def article_list():
    form = ArticleSearchForm()
    q = request.args.get('q')
    page = request.args.get('page', 1)
    if q is not None:
        # condition = {request.form['field']: q}
        form_field = request.args.get('field')
        form_order = request.args.get('order')
        print(q, page, form_field, form_order)
        if form_field == 'title':
            condition = Article.title.like('%%%s%%' % q)
        else:
            condition = Article.content.like('%%%s%%' % q)
        if form_order == '1':
            order = Article.id.asc()
        else:
            order = Article.id.desc()
        res = Article.query.filter(condition).order_by(order).paginate(int(page), 10)
        articles = res.items
        pageList = res.iter_pages()
        total = res.total
        pages = res.pages
        # 有条件搜索和无搜索转到同一模板，用模板语法来区分get的链接
        return render_template('admin/article/article_list.html', articles=articles, pageList=pageList,
                               total=total,
                               pages=pages, form=form, q=q, field=form_field, order=form_order)
    else:
        res = Article.query.order_by(Article.id.desc()).paginate(int(page), 10)
        # 无论搜索还是默认查看，都是翻页处理
        articles = res.items
        pageList = res.iter_pages()
        total = res.total
        pages = res.pages
        # 有条件搜索和无搜索转到同一模板，用模板语法来区分get的链接
        return render_template("admin/article/article_list.html", articles=articles, pageList=pageList, total=total,
                               pages=pages, form=form)


# 根据文章id删除文章
@admin_app.route('/article/delete/', methods=['post'])
def article_delete():
    csrf.protect()
    article_id = int(request.form.get('article_id'))
    message = {}
    article = Article.query.get(article_id)
    try:
        db.session.delete(article)
        db.session.commit()
    except:
        message['result'] = 'fail'
    else:
        message['result'] = 'success'
    return jsonify(message)


# 文章修改
@admin_app.route('/article/edit/<int:article_id>', methods=['get', 'post'])
def article_edit(article_id):
    form = set_article_form()
    article = Article.query.get_or_404(article_id)
    message = {"result": ""}
    if form.validate_on_submit():
        article.cate_id = form.data['cate']
        article.title = form.data['title']
        article.thumb = form.data['thumb']
        article.intro = form.data['intro']
        article.content = form.data['content']
        try:
            db.session.add(article)
            db.session.commit()
            print('文章提交')
        except Exception as e:
            print(str(e))
            message['result'] = 'fail'
        else:
            message['result'] = 'success'
        return jsonify(message)
    elif form.errors:
        print(form.errors)
    else:
        form.cate.data = article.cate_id
        form.title.data = article.title
        form.thumb.data = article.thumb
        form.intro.data = article.intro
        form.content.data = article.content
    return render_template('admin/article/article_edit.html', article=article, form=form)


# 初始化文章表单类的分类选择，需要从数据库读取数据
def set_article_form():
    form = ArticleForm()
    form.cate.choices = [(row.cate_id, row.cate_name) for row in Category.query.all()]
    return form
