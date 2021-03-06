from flask import request, redirect, url_for, render_template, session, jsonify
from libs import db
from models import Article, Category
from .member_app import member_app
import json
from forms.article_form import ArticleForm, ArticleSearchForm


# 会员发布文章
@member_app.route("/article/post", methods=['get', 'post'])
def article_post():
    form = set_article_form()
    if form.validate_on_submit():
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
            message = {"message": "文章发布成功"}
        return jsonify(message)
    return render_template("member/article/article_post.html", form=form)


# 显示会员文章列表
@member_app.route("/article/list/", methods=['get', 'post'])
def article_list():
    form = ArticleSearchForm()
    q = request.args.get('q')
    page = request.args.get('page', 1)
    if q is not None:
        form_field = request.args.get('field')
        form_order = request.args.get('order')
        if form_field == 'title':
            condition = Article.title.like('%%%s%%' % q)
        else:
            condition = Article.content.like('%%%s%%' % q)
        if form_order == '1':
            order = Article.id.asc()
        else:
            order = Article.id.desc()
        res = Article.query.filter(Article.author == session['user']).filter(condition).order_by(order).paginate(
            int(page), 10)
        articles = res.items
        pageList = res.iter_pages()
        total = res.total
        pages = res.pages
        # 有条件搜索和无搜索转到同一模板，用模板语法来区分get的链接
        return render_template('member/article/article_list.html', articles=articles, pageList=pageList, total=total,
                               pages=pages, form=form, q=q, field=form_field, order=form_order)
    else:
        res = Article.query.filter(Article.author == session['user']).order_by(Article.id.desc()).paginate(
            int(page), 10)
        # 无论搜索还是默认查看，都是翻页处理
        articles = res.items
        pageList = res.iter_pages()
        total = res.total
        pages = res.pages
        # 有条件搜索和无搜索转到同一模板，用模板语法来区分get的链接
        return render_template("member/article/article_list.html", articles=articles, pageList=pageList, total=total,
                               pages=pages, form=form)


# 会员根据文章id删除文章
@member_app.route('/article/delete/<int:article_id>')
def article_delete(article_id):
    article = Article.query.get(article_id)
    # 只能删除自己的文章
    if article.author == session['user']:
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for('.article_list'))


# 会员修改文章
@member_app.route('/article/edit/<int:article_id>', methods=['get', 'post'])
def article_edit(article_id):
    form = set_article_form()
    article = Article.query.get(article_id)
    message = {'result': ''}
    if not article:
        return redirect(url_for('.article_list'))
    if form.validate_on_submit():
        # 只能修改自己的文章
        if article.author == session['user']:
            article.cate_id = form.data['cate']
            article.title = form.data['title']
            article.thumb = form.data['thumb']
            article.intro = form.data['intro']
            article.content = form.data['content']
            try:
                db.session.add(article)
                db.session.commit()
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
    return render_template('member/article/article_edit.html', article=article, form=form)


# 初始化文章表单类的分类选择，需要从数据库读取数据
def set_article_form():
    form = ArticleForm()
    form.cate.choices = [(row.cate_id, row.cate_name) for row in Category.query.all()]
    return form
