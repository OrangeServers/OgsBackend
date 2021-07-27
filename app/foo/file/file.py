import os
from flask import request, jsonify
from werkzeug.utils import secure_filename


class FileGet:
    def __init__(self):
        self.req_dir = request.values.get('req_dir', default='')
        self.def_dir_path = '/data/tmp/test'
        self.old_def_dir = self.def_dir_path + self.req_dir
        self.dir_list = []
        self.file_list = []

    def get_file_list(self):
        get_file_type = request.values.get('get_file_type')
        os.chdir(self.old_def_dir)
        if get_file_type == 'checkout':
            if os.getcwd() == '/data/tmp/test':
                os.chdir('/data/tmp/test')
                # 回退服务端逻辑待删除测试
            else:
                os.chdir('../')
        dir_list = os.listdir('./')
        is_path = os.getcwd()
        print(is_path)
        for i in dir_list:
            file_type = os.path.isfile(i)
            if file_type:
                self.file_list.append(i)
            else:
                self.dir_list.append(i)
        return jsonify({'file': self.file_list, 'dir': self.dir_list, 'ispath': is_path.partition('/data/tmp/test')[2] + '/'})

    def mkdir_file_name(self):
        os.chdir(self.old_def_dir)
        mk_filename = request.values.get('mk_filename')
        is_file = os.path.exists(mk_filename)
        if is_file:
            return jsonify({'status': 'fail', 'msg': '该文件已存在'})
        else:
            os.mkdir(mk_filename)
            return jsonify({'status': 'true', 'msg': '创建成功'})

    def change_file_name(self):
        new_dir = request.values.get('new_dir')
        is_file = os.path.exists(self.def_dir_path + new_dir)
        if is_file:
            return jsonify({'status': 'fail', 'msg': '修改名称失败，已有该名称'})
        else:
            os.rename(self.old_def_dir, self.def_dir_path + new_dir)
            return jsonify({'status': 'true', 'msg': '修改成功'})

    def remove_file(self):
        os.chdir(self.old_def_dir)
        rm_filename = request.values.get('rm_filename')
        file_type = os.path.isfile(rm_filename)
        if file_type:
            os.remove(rm_filename)
            return jsonify({'status': 'true', 'msg': '删除了一个文件'})
        else:
            os.rmdir(rm_filename)
            return jsonify({'status': 'true', 'msg': '删除了一个目录'})

    def save_file(self):
        os.chdir(self.old_def_dir)
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        file.save(filename)
        return jsonify({'status': 'true'})
