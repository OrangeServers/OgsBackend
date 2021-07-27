import os, sys, json
from flask import request, Response


class DownloadFile:
    """
        文件下载接口
    :post传值下载文件
    """
    def __init__(self):
        self.file_path = '/data/tmp/test'
        self.file_name = request.values.get('filename')

    @staticmethod
    def file_iterator(file_path, chunk_size=512):
        """
            文件读取迭代器
        :param file_path:文件路径
        :param chunk_size: 每次读取流大小
        :return:
        """
        with open(file_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(chunk_size)
                if chunk:
                    yield chunk
                else:
                    break

    @staticmethod
    def to_json(obj):
        """
            放置
        :return:
        """
        return json.dumps(obj, ensure_ascii=False)

    def download(self):
        """
            文件下载
        :return:
        """
        if self.file_path is None:
            return self.to_json({'status': 'fail', 'msg': '请输入参数'})
        else:
            if self.file_path == '':
                return self.to_json({'status': 'fail', 'msg': '请输入正确路径'})
            else:
                if not os.path.isfile(self.file_path + self.file_name):
                    return self.to_json({'status': 'fail', 'msg': '文件路径不存在'})
                else:
                    filename = os.path.basename(self.file_path + self.file_name)
                    response = Response(self.file_iterator(self.file_path + self.file_name))
                    response.headers['Content-Type'] = 'application/octet-stream'
                    response.headers["Content-Disposition"] = 'attachment;filename="{}"'.format(filename)
                    return response
