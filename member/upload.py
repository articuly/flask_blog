import os
import json
from flask import request, render_template, current_app, session
from .member_app import member_app
from views.upload import get_dir, create_filename


# 会员用户使用JQ方式上传文件
@member_app.route('/upload', methods=['get', 'post'])
def upload():
    if request.method == 'POST':
        file_storage_list = request.files.getlist('file')
        message = {'result': '', 'error': '', 'filepath_list': []}
        print(file_storage_list)
        print(request.content_length)  # 上传长度
        if request.content_length > 10240 * 1024:
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
    return render_template('member/upload/jquery_upload.html')
