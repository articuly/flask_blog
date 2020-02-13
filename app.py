from flask import Flask, render_template
from flask import request, redirect, url_for, session, make_response
from flask_migrate import Migrate
from models import User, Category, Article
from libs import db
from views.users import user_app
from views.articles import article_app
from settings import config
from admin import admin_app
from member import member_app

app = Flask(__name__)
app.config.from_object(config['development'])

db.init_app(app)
# 注册功能的蓝印
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(member_app, url_prefix='/member')
app.register_blueprint(user_app, url_prefix='/user')
app.register_blueprint(article_app, url_prefix='/article')


@app.route('/<int:page>')
@app.route('/', defaults={'page': 1})
def html(page):
    res = Article.query.order_by(Article.id.desc()).paginate(page, 10)
    articles = res.items
    pageList = res.iter_pages()
    return render_template('index.html', page=page, articles=articles, pageList=pageList)


@app.route('/index')
def index():
    return redirect(url_for('html'))


@app.route('/login', methods=['get', 'post'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            session['user'] = user.username
            print(f'{username} 登陆成功')
            # 登录成功返回首页
            return redirect(url_for('index'))
        else:
            # 登录失败，给出提示
            message = '用户名与密码不匹配'
    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
    return redirect(url_for('index'))


# 上下文处理函数
@app.context_processor
def account():
    username = session.get('user')
    return {'username': username}


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


@app.route('/test_cookie')
def test_cookie():
    username = request.cookies.get('username')
    response = make_response('<b>' + str(username) + '</b>')
    response.set_cookie('number', '10')
    # return '<b>' + str(username) + '</b>'
    return response


@app.route('/test_cookie2')
def test_cookie2():
    number = request.cookies.get('number', '0')
    number = int(number) + 1
    username = request.cookies.get('username')
    response = make_response('<b>number=' + str(number) + '</b>')
    response.set_cookie('number', str(number))
    return response


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
