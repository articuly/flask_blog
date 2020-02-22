from flask import redirect, url_for, render_template, request
from models import Article, Category, Alert
from flask import Blueprint

article_app = Blueprint('article_app', __name__)


# 根据文章id阅读文章
@article_app.route('/view/<int:article_id>')
def view(article_id):
    article = Article.query.get(article_id)
    if not article:
        return redirect(url_for('article_app.list'))
    return render_template('article/detail.html', article=article)


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
