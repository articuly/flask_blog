from flask import redirect, url_for, render_template, request, session, jsonify
from models import Article, Category, Alert, Comment
from libs import db
from flask import Blueprint
from forms.article_form import CommentForm

article_app = Blueprint('article_app', __name__)


# 根据文章id阅读文章并显示评论功能
@article_app.route('/view/<int:article_id>', methods=['get', 'post'])
def view(article_id):
    article = Article.query.get(article_id)
    if not article:  # 没有找到文章跳到主页
        return redirect(url_for('html'))

    # 只显示最新15条已审核的与文章ID相同的文章评论
    comments = Comment.query.filter(Comment.article_id == article_id).filter(Comment.audited == 1).order_by(
        Comment.time.desc()).limit(15)
    print(comments.count(), '条评论')

    # 发表评论功能，有用户登陆才显示表单
    if 'user' in session:
        form = CommentForm()
        message = {'result': 'fail'}
        if form.validate_on_submit():
            content = form.data['content']
            comment = Comment(
                author=session['user'],
                article_id=article.id,
                content=content
            )
            try:
                db.session.add(comment)
                db.session.commit()
            except Exception as e:
                print(str(e))
            else:
                message = {'result': 'success'}
            return jsonify(message)
        elif form.errors:
            print(form.errors)
            message.update(form.errors)
            return jsonify(message)
        else:
            return render_template('article/detail.html', article=article, comments=comments, form=form)
    return render_template('article/detail.html', article=article, comments=comments)


# 根据文章cate_id显示文章列表
@article_app.route('/cate/<int:cate_id>/<int:page>')
@article_app.route('/', defaults={'cate_id': 0, 'page': 1})
def getArticleList(cate_id, page):
    # 提取最新的公告
    alert = Alert.query.order_by(Alert.alert_id.desc()).first()

    # 提取所有推荐值前15的文章
    recommend_articles = Article.query.filter(Article.is_recommend != None).order_by(Article.is_recommend.desc()).limit(
        15)

    # 导航栏搜索功能
    q = request.args.get('nav_search')
    if request.method == 'GET' and q is not None and q != '':
        print('nav_search', q)
        page = request.args.get('page', 1)
        res = Article.query.filter(Article.content.like('%%%s%%' % q)).order_by(Article.id.desc()).paginate(int(page),
                                                                                                            15)
        articles = res.items
        pageList = res.iter_pages()
        total = res.total
        return render_template('search_articles.html', articles=articles, pageList=pageList, total=total, page=page,
                               q=q, recommend_articles=recommend_articles)

    # 显示分类文章
    if cate_id == 0:
        res = Article.query.order_by(Article.id.desc()).paginate(page, 15)
    else:
        res = Article.query.order_by(Article.id.desc()).filter_by(cate_id=cate_id).paginate(page, 15)
    category = Category.query.get(cate_id)
    articles = res.items
    pageList = res.iter_pages()
    return render_template('article/cate_articles.html', cate_id=cate_id, articles=articles, pageList=pageList,
                           category=category, res=res, alert=alert, recommend_articles=recommend_articles)
