from flask import request, redirect, url_for, render_template
from libs import db
from models import Article
from flask import Blueprint

article_app=Blueprint('article_app', __name__)

@article_app.route("/post", methods=['get', 'post'])
def post():
    message = None
    if request.method=="POST":
        title= request.form['title']
        intro=request.form['intro']
        content=request.form['content']
        article=Article(
            title=title,
            intro=intro,
            content=content,
            author='admin'
        )
        db.session.add(article)
        db.session.commit()
        message="文章发布成功"
    return render_template("article/post.html", message=message)

@article_app.route("/list/<int:page>", methods=['get', 'post'])
@article_app.route("/list", defaults={"page":1}, methods=['get', 'post'])
def list(page):
    # if request.method=='POST':
    #     q=request.form['q']
    res=Article.query.paginate(page, 10)
    return render_template("article/article_list.html")