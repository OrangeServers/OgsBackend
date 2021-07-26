import os
from flask import request, jsonify


class FileGet:
    def __init__(self):
        self.req_dir = request.values.get('req_dir', default='')
        self.def_dir_path = '/data/tmp/test/'
        self.old_def_dir = self.def_dir_path + self.req_dir
        self.dir_list = []
        self.file_list = []

    def get_file_list(self):
        dir_list = os.listdir(self.old_def_dir)
        for i in dir_list:
            file_type = os.path.isfile(self.old_def_dir + i)
            if file_type:
                self.file_list.append(i)
            else:
                self.dir_list.append(i)
        return jsonify({'file': self.file_list, 'dir': self.dir_list})

    def change_file_name(self):
        new_dir = request.values.get('new_dir')
        is_file = os.path.exists(self.def_dir_path + new_dir)
        if is_file:
            return jsonify({'status': 'fail', 'msg': '修改名称失败，已有该名称'})
        else:
            os.rename(self.old_def_dir, self.def_dir_path + new_dir)
            return jsonify({'status': 'true', 'msg': '修改成功'})

    def remove_file(self):
        file_type = os.path.isfile(self.old_def_dir)
        if file_type:
            os.remove(self.old_def_dir)
            return jsonify({'status': 'true', 'msg': '删除了一个文件'})
        else:
            os.rmdir(self.old_def_dir)
            return jsonify({'status': 'true', 'msg': '删除了一个目录'})
