import os, sys, json
from flask import request, Response


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


def to_json(obj):
    """
        放置
    :return:
    """
    return json.dumps(obj, ensure_ascii=False)


def download():
    """
        文件下载
    :return:
    """
    file_path = '/data/tmp/test/'
    file_name = request.values.get('filename')
    if file_path is None:
        return to_json({'success': 0, 'message': '请输入参数'})
    else:
        if file_path == '':
            return to_json({'success': 0, 'message': '请输入正确路径'})
        else:
            if not os.path.isfile(file_path + file_name):
                return to_json({'success': 0, 'message': '文件路径不存在'})
            else:
                filename = os.path.basename(file_path + file_name)
                response = Response(file_iterator(file_path + file_name))
                response.headers['Content-Type'] = 'application/octet-stream'
                response.headers["Content-Disposition"] = 'attachment;filename="{}"'.format(filename)
                return response
