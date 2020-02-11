import os
import json
from flask import Blueprint, request, render_template, current_app
from libs import login_required
from flask import jsonify

upload_app = Blueprint('upload', __name__)


@upload_app.route('/by_ajax', methods=['get', 'post'])
def upload():
    if request.method == 'POST':
        file_storage_list = request.files.getlist('file')
        message = {'result': '', 'error': '', 'filepath_list': []}
        print(file_storage_list)
        print(request.content_length)  # 上传长度
        if request.content_length > 102400 * 1024:
            message['result'] = 'fail'
            message['error'] = '上传所有文件太大'
            return json.dumps(message)
        for file_storage in file_storage_list:
            print(file_storage.content_type)  # 上传类型
            # 如果上传类型不在允许的类型内，则返回403错误
            if file_storage.content_type not in current_app.config['ALLOW_UPLOAD_TYPE']:
                message['result'] = 'fail'
                message['error'] = '上传文件类型不对'
                return json.dumps(message)
            print(file_storage.filename)  # 上传原文件名
            file_path = os.path.join(get_dir(), create_filename(file_storage.filename))
            try:
                file_storage.save(file_path)
            except Exception as e:
                message = {'result': 'fail', 'error': str(e)}
                return json.dumps(message)
            # [1:]将.static/相对路径转为/static绝对路径
            print(file_path)
            print(file_path[1:])
            message['filepath_list'].append(file_path[1:])
        message['result'] = 'success'
        return json.dumps(message)
    return render_template('upload/jquery_upload.html')


@upload_app.route('/by_form', methods=['get', 'post'])
def uploadByForm():
    if request.method == 'POST':
        file_storage_list = request.files.getlist('file')
        print(file_storage_list)
        print(request.content_length)  # 上传长度
        if request.content_length > 10240 * 1024:  # 如果上传数据长度大于10M，则返回403错误
            return "", 403
        for file_storage in file_storage_list:
            print(file_storage.content_type)  # 上传类型
            # 如果上传类型不在允许的类型内，则返回403错误
            if file_storage.content_type not in current_app.config['ALLOW_UPLOAD_TYPE']:
                return "", 403
            print(file_storage.filename)  # 上传原文件名
            file_path = os.path.join(get_dir(), create_filename(file_storage.filename))
            file_storage.save(file_path)
    return render_template('upload/form_upload.html')


@upload_app.route('/by_xhr', methods=['get', 'post'])
def uploadByXhr():
    if request.method == 'POST':
        file_storage_list = request.files.getlist('file')
        message = {'result': '', 'error': '', 'filepath_list': []}
        print(file_storage_list)
        print(request.content_length)  # 上传长度
        if request.content_length > 102400 * 1024:
            message['result'] = 'fail'
            message['error'] = '上传所有文件太大'
            return json.dumps(message)
        for file_storage in file_storage_list:
            print(file_storage.content_type)  # 上传类型
            # 如果上传类型不在允许的类型内，则返回403错误
            if file_storage.content_type not in current_app.config['ALLOW_UPLOAD_TYPE']:
                message['result'] = 'fail'
                message['error'] = '上传文件类型不对'
                return json.dumps(message)
            print(file_storage.filename)  # 上传原文件名
            file_path = os.path.join(get_dir(), create_filename(file_storage.filename))
            try:
                file_storage.save(file_path)
            except Exception as e:
                message = {'result': 'fail', 'error': str(e)}
                return json.dumps(message)
            # [1:]将.static/相对路径转为/static绝对路径
            print(file_path)
            print(file_path[1:])
            message['filepath_list'].append(file_path[1:])
        message['result'] = 'success'
        return json.dumps(message)
    return render_template('upload/xhr_upload.html')


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


@upload_app.route('/ckeditor/browser', methods=['get'])
def ckeditor_browser():
    images = []
    for dirpath, dirnames, filenames in os.walk('./static/uploads'):
        print(dirpath, dirnames, filenames, sep='>>>')
        for file in filenames:
            images.append(os.path.join(dirpath[1:], file))
    return render_template('upload/browser.html', images=images)


def get_dir():
    '''
    生成文件存放路经
    返回存放文件路经
    '''
    from datetime import date
    base_path = './static/uploads'  # 上传文件存放路经
    d = date.today()  # 根据上传的日期存放
    path = os.path.join(base_path, str(d.year), str(d.month))  # 生成存储路经
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
