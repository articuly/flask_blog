from flask import request, render_template, jsonify
from libs import db
from models import Comment, Article
from .admin_app import admin_app


# 显示审核后的评论，包括通过和不通过的
@admin_app.route("/comment/list/<int:page>", methods=['get', 'post'])
@admin_app.route("/comment/list/", defaults={'page': 1}, methods=['get', 'post'])
def comment_list(page):
    res = Comment.query.filter(Comment.audited != None).order_by(Comment.time.desc()).paginate(page, 20)
    audited_comment = Comment.query.filter(Comment.audited == 1).count()
    failed_comment = Comment.query.filter(Comment.audited == 2).count()
    comments = res.items
    pageList = res.iter_pages()
    total = res.total
    pages = res.pages
    return render_template("admin/comment/comment_list.html", comments=comments, pageList=pageList, total=total,
                           pages=pages, audited_comment=audited_comment, failed_comment=failed_comment)


# 显示未审核的评论，以便管理员审核
@admin_app.route("/comment/audit/<int:page>", methods=['get', 'post'])
@admin_app.route("/comment/audit/", defaults={'page': 1}, methods=['get', 'post'])
def comment_audit(page):
    res = Comment.query.filter(Comment.audited == None).order_by(Comment.time.desc()).paginate(page, 30)
    not_audit = Comment.query.filter(Comment.audited == None).count()
    comments = res.items
    pageList = res.iter_pages()
    total = res.total
    pages = res.pages
    return render_template("admin/comment/comment_audit.html", comments=comments, pageList=pageList, total=total,
                           pages=pages, not_audit=not_audit)


# 审核后通过的评论
@admin_app.route('/comment/audited/', methods=['post'])
def audited():
    print('audited')
    comment_id = int(request.form.get('comment_id'))
    message = {'result': 'fail', 'id': comment_id, 'type': 'audited'}
    if comment_id:
        comment = Comment.query.get(comment_id)
        if comment:
            comment.audited = 1  # 审核通过为1
            try:
                db.session.commit()
            except Exception as e:
                print(str(e))
            else:
                message['result'] = 'success'
    return jsonify(message)


# 审核后通过的评论
@admin_app.route('/comment/failed/', methods=['post'])
def failed():
    comment_id = int(request.form.get('comment_id'))
    message = {'result': 'fail', 'id': comment_id, 'type': 'failed'}
    if comment_id:
        comment = Comment.query.get(comment_id)
        if comment:
            comment.audited = 2  # 审核通过为2
            try:
                db.session.commit()
            except Exception as e:
                print(str(e))
            else:
                message['result'] = 'success'
    return jsonify(message)


# 审核后通过的评论
@admin_app.route('/comment/delComment/', methods=['post'])
def delComment():
    comment_id = int(request.form.get('comment_id'))
    message = {'result': 'fail', 'id': comment_id, 'type': 'del'}
    if comment_id:
        comment = Comment.query.get(comment_id)
        if comment:
            try:
                db.session.delete(comment)
                db.session.commit()
            except Exception as e:
                print(str(e))
            else:
                message['result'] = 'success'
    return jsonify(message)
