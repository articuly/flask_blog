from flask import redirect, url_for, render_template, request
from models import Alert
from .admin_app import admin_app
from libs import db


# 显示公告列表和增加公告功能
@admin_app.route("/alert/list/", methods=['get', 'post'])
def alert_list():
    alerts = Alert.query.order_by(Alert.alert_id.desc()).all()
    if request.method == 'POST':
        content = request.form['alert']
        alert = Alert(alert_content=content)
        db.session.add(alert)
        db.session.commit()
        return redirect(url_for("admin_app.alert_list"))
    return render_template('admin/alert/alert_list.html', alerts=alerts)


# 根据alert_id删除对应的公告
@admin_app.route('/alert/remove/<int:alert_id>')
def alert_remove(alert_id):
    alert = Alert.query.get(alert_id)
    try:
        db.session.delete(alert)
        db.session.commit()
    except Exception as e:
        print(str(e))
    return redirect(url_for('admin_app.alert_list'))
