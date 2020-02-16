from flask import session, redirect, url_for, render_template
from flask import Blueprint
from libs import login_required

admin_app = Blueprint('admin_app', __name__)

# 请求会先执行is_admin()，只要访问admin_app就会检查
@admin_app.before_request
@login_required
def is_admin():
    print(session['user'])
    if session['user'] != 'admin':
        print('user is someone else.')
        return redirect(url_for('login'))


@admin_app.route('/')
def admin_index():
    return render_template('admin/admin_index.html')
