from flask import request, redirect, url_for, render_template, session
from libs import db
from models import Article, Category
from .member_app import member_app
import json
from forms.article_form import ArticleForm, ArticleSearchForm


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
        db.session.add(article)
        db.session.commit()
        message = {"message": "文章发布成功"}
        return json.dumps(message)
    return render_template("member/article/article_post.html")


@member_app.route("/article/list/<int:page>", methods=['get', 'post'])
@member_app.route("/article/list", defaults={"page": 1}, methods=['get', 'post'])
def article_list(page):
    if request.method == 'POST':
        q = request.form['q']
        condition = {request.form['field']: q}
        if request.form['field'] == 'title':
            condition = Article.title.like('%%%s%%' % q)
        else:
            condition = Article.content.like('%%%s%%' % q)
        if request.form['order'] == '1':
            order = Article.id.asc()
        else:
            order = Article.id.desc()
        res = Article.query.filter(Article.author == session['user']).filter(condition).order_by(order).paginate(page,
                                                                                                                 10)
    else:
        res = Article.query.filter(Article.author == session['user']).paginate(page, 10)
    # 无论搜索还是默认查看，都是翻页处理
    articles = res.items
    pageList = res.iter_pages()
    total = res.total
    pages = res.pages
    return render_template("member/article/article_list.html", articles=articles, pageList=pageList, total=total,
                           pages=pages)


# 根据文章id删除文章
@member_app.route('/article/delete/<int:article_id>')
def article_delete(article_id):
    article = Article.query.get(article_id)
    # 只能删除自己的文章
    if article.author == session['user']:
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for('.article_list'))


# 文章修改
@member_app.route('/article/edit/<int:article_id>', methods=['get', 'post'])
def article_edit(article_id):
    form = set_article_form()
    article = Article.query.get(article_id)
    if not article:
        return redirect(url_for('.article_list'))
    if request.method == 'POST':
        # 只能修改自己的文章
        if article.author == session['user']:
            article.cate_id = request.form['cate']
            article.title = request.form['title']
            article.intro = request.form['intro']
            article.content = request.form['content']
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('.article_list'))
    return render_template('member/article/article_edit.html', article=article, form=form)


def set_article_form():
    form = ArticleForm()
    form.cate.choices = [(row.cate_id, row.cate_name) for row in Category.query.all()]
    return form
