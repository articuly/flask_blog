from flask import request, redirect, url_for, render_template
from libs import db
from models import Article
from flask import Blueprint

article_app = Blueprint('article_app', __name__)


@article_app.route("/post", methods=['get', 'post'])
def post():
    message = None
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        content = request.form['content']
        article = Article(
            title=title,
            intro=intro,
            content=content,
            author='admin'
        )
        db.session.add(article)
        db.session.commit()
        message = "文章发布成功"
    return render_template("article/post.html", message=message)


@article_app.route("/list/<int:page>", methods=['get', 'post'])
@article_app.route("/list", defaults={"page": 1}, methods=['get', 'post'])
def list(page):
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
        res = Article.query.filter(condition).order_by(order).paginate(page, 10)
    else:
        res = Article.query.paginate(page, 10)
    # 无论搜索还是默认查看，都是翻页处理
    articles = res.items
    pageList = res.iter_pages()
    total = res.total
    pages = res.pages
    return render_template("article/article_list.html", articles=articles, pageList=pageList, total=total, pages=pages)


# 根据文章id删除文章
@article_app.route('/delete/<int:article_id>')
def delete(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('article_app.list'))


# 根据文章id阅读文章
@article_app.route('/view/<int:article_id>')
def view(article_id):
    article = Article.query.get(article_id)
    if not article:
        return redirect(url_for('article_app.list'))
    return render_template('article/detail.html', article=article)


# 文章修改
@article_app.route('/edit/<int:article_id>', methods=['get', 'post'])
def edit(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.content = request.form['content']
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('article_app.list'))
    return render_template('article/edit_article.html', article=article)
