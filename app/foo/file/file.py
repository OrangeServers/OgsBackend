import os
from flask import request, jsonify


class FileGet:
    def __init__(self):
        self.req_dir = request.values.get('req_dir', default='')
        self.def_dir_path = '/data/putfile/' + self.req_dir
        self.dir_m = {}
        self.file_m = {}

    def get_file_list(self):
        dir_list = os.listdir(self.def_dir_path)
        for i in dir_list:
            file_type = os.path.isfile(self.def_dir_path + i)
            if file_type:
                self.file_m[i] = {'name': i, 'type': 'file'}
            else:
                self.dir_m[i] = {'name': i, 'type': 'dir'}
        return jsonify({'file': self.file_m, 'dir': self.dir_m})
