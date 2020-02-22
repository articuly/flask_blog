from flask import Flask, render_template
from flask import request, redirect, url_for, session, make_response
from flask_migrate import Migrate
from models import User, Category, Article, Alert
from libs import db, ckeditor, csrf, dropzone
from settings import config
from views.users import user_app
from views.articles import article_app
from views.upload import upload_app
from admin import admin_app
from member import member_app
from forms.account_form import LoginForm

# 实例化Flask
app = Flask(__name__)
app.config.from_object(config['development'])

# 初始化各种插件
db.init_app(app)
ckeditor.init_app(app)
csrf.init_app(app)
dropzone.init_app(app)

# 注册蓝图功能
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(member_app, url_prefix='/member')
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(article_app, url_prefix='/article')
app.register_blueprint(upload_app, url_prefix="/upload")


@app.route('/<int:page>')
@app.route('/', defaults={'page': 1})
def html(page):
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
                               q=q)
    res = Article.query.order_by(Article.id.desc()).paginate(page, 10)
    alert = Alert.query.order_by(Alert.alert_id.desc()).first()
    articles = res.items
    pageList = res.iter_pages()
    # print(dir(articles))
    # print(dir(pageList))
    # print(dir(res))
    return render_template('index.html', page=page, articles=articles, pageList=pageList, res=res, alert=alert)


# index指向根路经
@app.route('/index')
def index():
    return redirect(url_for('html'))


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    message = None
    # if request.method == 'POST':  # 不能验证提交的数据
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        user = User.query.filter_by(username=username).first()
        # 验证密码
        if user and user.validate_password(password):
            session['user'] = user.username
            print(f'{username} 登陆成功')
            # 登录成功返回首页
            return redirect(url_for('index'))
        else:
            # 登录失败，给出提示
            message = '用户名与密码不匹配'
    else:
        print(form.errors)
    return render_template('login.html', message=message, form=form)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')  # 删除session中的用户
    return redirect(url_for('index'))


# 上下文处理函数，全局传出的模板变量username
@app.context_processor
def account():
    username = session.get('user')
    return {'username': username}


# 上下文处理函数，全局传出的模板变量cates
@app.context_processor
def getCateList():
    cates = Category.query.all()
    return {'cates': cates}


# 测试功能
@app.route('/test')
def test():
    try:
        number += 1
    except Exception:
        number = 0
    return 'number=' + str(number)


# 测试cookie
@app.route('/test_cookie')
def test_cookie():
    username = request.cookies.get('username')
    response = make_response('<b>' + str(username) + '</b>')
    response.set_cookie('number', '10')
    # return '<b>' + str(username) + '</b>'
    return response


# 测试cookie修改
@app.route('/test_cookie2')
def test_cookie2():
    number = request.cookies.get('number', '0')
    number = int(number) + 1
    username = request.cookies.get('username')
    response = make_response('<b>number=' + str(number) + '</b>')
    response.set_cookie('number', str(number))
    return response


# 测试session
@app.route('/test_session')
def test_session():
    try:
        session['number'] += 1
    except:
        session['number'] = 0
    return 'number=' + str(session['number'])


# 添加render_as_batch=True  SQLite支持批处理修改
# 但是这种如果修改多个字段，可能在发生错误时，发生修改不一致
migrate = Migrate(app, db, render_as_batch=True)
