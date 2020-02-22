from flask import session, render_template
from flask import Blueprint
from libs import login_required

member_app = Blueprint('member_app', __name__)


# 会员功能必须登陆
@member_app.before_request
@login_required
def is_login():
    print(session['user'])


# 会员功能主页
@member_app.route('/')
def member_index():
    print('hello')
    return render_template('member/member_index.html')
