import os
from flask import Blueprint, request, render_template, session
from flask import current_app
import json
from libs import login_required

upload_app = Blueprint("upload_app", __name__)


# 上传请求前调用的装饰器，判断是否有用户登陆
@upload_app.before_request
@login_required
def is_login():
    pass


# CKEditor的上传功能
@upload_app.route('/ckeditor', methods=['post'])
def ckeditor_upload():
    if request.method == 'POST':
        file_storage = request.files.get('upload')
        message = {
            'uploaded': "0",
            'fileName': "",
            'url': "",
            'error': {
                'message': ""
            }
        }
        # 获得上传数据长度
        if request.content_length > 10240 * 1024:
            message['uploaded'] = '0'
            message['error']['message'] = '上传文件太大'
            return json.dumps(message)
        if file_storage.content_type not in current_app.config['ALLOW_UPLOAD_TYPE']:
            message['uploaded'] = '0'
            message['error']['message'] = '上传文件类型不对'
            return json.dumps(message)
        file_path = os.path.join(get_dir(), create_filename(file_storage.filename))
        try:
            file_storage.save(file_path)
        except Exception as e:
            message = {'uploaded': '0', 'error': str(e)}
            return json.dumps(message)

        message['fileName'] = file_storage.filename
        message['url'] = file_path[1:]
        message['uploaded'] = '1'
        return json.dumps(message)


# CKEditor的上传后文件浏览功能
@upload_app.route('/ckeditor/browser', methods=['get'])
def ckeditor_browser():
    images = []
    for dirpath, dirnames, filenames in os.walk('./static/uploads/{0}'.format(session['user'])):
        print(dirpath, dirnames, filenames, sep='>>>')
        for file in filenames:
            images.append(os.path.join(dirpath[1:], file))
    return render_template('admin/upload/browser.html', images=images)


def get_dir():
    '''
    生成文件存放路经
    返回存放文件路经
    '''
    from datetime import date
    base_path = './static/uploads'  # 上传文件存放路经
    d = date.today()  # 根据上传的日期存放
    # 生成存储路经，储存在用户名的目录下，没有登陆的用户不能调用上传功能
    path = os.path.join(base_path, session['user'], str(d.year), str(d.month))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def create_filename(filename):
    '''
    生成随机文件名
    :arg filename
    '''
    import uuid
    ext = os.path.splitext(filename)[1]
    new_file_name = str(uuid.uuid4()) + ext
    return new_file_name
