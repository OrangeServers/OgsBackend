import os, psutil
from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.conf.conf_test import FILE_CONF


class FileGet:
    def __init__(self):
        self.req_dir = request.values.get('req_dir', default='')
        # self.def_dir_path = '/data/tmp/test'
        self.def_dir_path = FILE_CONF['file_path']
        self.old_def_dir = self.def_dir_path + self.req_dir
        self.dir_list = []
        self.file_list = []

    def get_file_list(self):
        # 磁盘操作
        disk_msg = psutil.disk_usage(self.def_dir_path)
        disk_total = round(disk_msg.total / 1024 / 1024 / 1024)
        disk_used = round(disk_msg.used / 1024 / 1024 / 1024)
        disk_free = round(disk_msg.free / 1024 / 1024 / 1024)
        # 文件列表操作
        get_file_type = request.values.get('get_file_type')
        os.chdir(self.old_def_dir)
        if get_file_type == 'checkout':
            if os.getcwd() == self.def_dir_path:
                os.chdir(self.def_dir_path)
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
        return jsonify(
            {'file': self.file_list, 'dir': self.dir_list, 'ispath': is_path.partition(self.def_dir_path)[2] + '/',
             'disk': {'total': disk_total, 'used': disk_used, 'free': disk_free}})

    def get_file_size(self):
        si_filename = request.values.get('si_filename')
        os.chdir(self.old_def_dir)
        file_size = os.path.getsize(si_filename)
        if file_size / 1024 < 1:
            return jsonify({'filename': si_filename, 'size': str(file_size) + 'B'})
        elif file_size / 1024 >= 1 and file_size / 1024 / 1024 < 1:
            return jsonify({'filename': si_filename, 'size': str(round(file_size / 1024)) + 'KB'})
        elif file_size / 1024 / 1024 >= 1 and file_size / 1024 / 1024 / 1024 < 1:
            return jsonify({'filename': si_filename, 'size': str(round(file_size / 1024 / 1024)) + 'MB'})
        elif file_size / 1024 / 1024 / 1024 >= 1 and file_size / 1024 / 1024 / 1024 / 1024 < 1:
            return jsonify({'filename': si_filename, 'size': str(round(file_size / 1024 / 1024 / 1024)) + 'GB'})
        elif file_size / 1024 / 1024 / 1024 / 1024 >= 1 and file_size / 1024 / 1024 / 1024 / 1024 / 1024 < 1:
            return jsonify({'filename': si_filename, 'size': str(round(file_size / 1024 / 1024 / 1024 / 1024)) + 'TB'})

    def mkdir_file_name(self):
        mk_filename = request.values.get('mk_filename')
        os.chdir(self.old_def_dir)
        is_file = os.path.exists(mk_filename)
        if is_file:
            return jsonify({'status': 'fail', 'msg': '该文件已存在'})
        else:
            os.mkdir(mk_filename)
            return jsonify({'status': 'true', 'msg': '创建成功'})

    def change_file_name(self):
        old_name = request.values.get('old_name')
        new_name = request.values.get('new_name')
        os.chdir(self.old_def_dir)
        is_file = os.path.exists(new_name)
        if is_file:
            return jsonify({'status': 'fail', 'msg': '修改名称失败，已有该名称'})
        else:
            os.rename(old_name, new_name)
            return jsonify({'status': 'true', 'msg': '修改成功'})

    def remove_file(self):
        rm_filename = request.values.get('rm_filename')
        os.chdir(self.old_def_dir)
        file_type = os.path.isfile(rm_filename)
        if file_type:
            os.remove(rm_filename)
            return jsonify({'status': 'true', 'msg': '删除了一个文件'})
        else:
            os.rmdir(rm_filename)
            return jsonify({'status': 'true', 'msg': '删除了一个目录'})

    def save_file(self):
        file = request.files.get('file')
        os.chdir(self.old_def_dir)
        filename = secure_filename(file.filename)
        file.save(filename)
        return jsonify({'status': 'true'})
