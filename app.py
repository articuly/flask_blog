from flask import Flask, render_template
from flask import request, redirect, url_for, session
from flask_migrate import Migrate
from models import User
from libs import db
from views.users import user_app
from views.articles import article_app

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"  ## ///为相对路经，////为绝对路经
app.secret_key = "123654"

db.init_app(app)

app.register_blueprint(user_app, url_prefix="/user")
app.register_blueprint(article_app, url_prefix='/article')

@app.route('/')
def html():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['get', 'post'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.username
            print(f'{username} 登陆成功')
            # 登录成功返回首页
            return redirect(url_for('index'))
        else:
            # 登录失败，给出提示
            message = '用户名与密码不匹配'
    return render_template('login.html', message=message)


@app.context_processor
def account():
    username = session.get('user')
    return {'username': username}


migrate = Migrate(app, db, render_as_batch=True)
