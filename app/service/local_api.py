from flask import jsonify
from app.foo.local.Basics import DataList, DataSumAll, CountList, CountUpdate, GetUserImage, PutUserImage
from app.foo.local.LocalShell import LocalDirList, LocalFilePut
from app.conf.conf_test import DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH, RSYNC_SHELL_CMD
from app.foo.local.LocalInit import AppInit
from app.foo.ssh.webssh import OgsWebSocket
from app.foo.local.Settings import OgsSettings
from app.foo.local.download import DownloadFile
from app.foo.file.file import FileGet


# 初始化：
def local_app_init():
    orange = AppInit()
    orange.con_init()


def local_app_status():
    orange = AppInit()
    return orange.app_status()


def count_list():
    orange = CountList()
    return orange.server_count_all


def local_chart_count_all():
    orange = CountList()
    return orange.server_chart_count_all


def local_chart_into():
    orange = CountUpdate()
    return orange.count_into_all


def local_chart_update():
    orange = CountUpdate()
    return orange.count_update_all


def local_dir_group():
    orange = LocalDirList()
    return jsonify({'group_dir_msg': orange.cmdlist_shell(DEFAULT_DIR1_PATH)})


def local_dir_project():
    orange = LocalDirList(DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH)
    return orange.getdir1()


def local_rsync_code():
    orange = LocalDirList(DEFAULT_DIR1_PATH, DEFAULT_DIR2_PATH, RSYNC_SHELL_CMD)
    return orange.getdir2()


def local_data_sum():
    orange = DataSumAll()
    return orange.get_sum()


def local_data_list():
    orange = DataList()
    return orange.get_list()


def local_data_file_put():
    orange = LocalFilePut()
    return orange.put_file()


def local_image_get(img_name):
    orange = GetUserImage()
    return orange.get_img(img_name)


def local_image_put():
    orange = PutUserImage()
    return orange.put_img()


def local_web_ssh():
    orange = OgsWebSocket()
    return orange.web_ssh()


def local_settings_get():
    orange = OgsSettings()
    return orange.settings_info()


def local_settings_update():
    orange = OgsSettings()
    return orange.settings_change()


def file_download():
    orange = DownloadFile()
    return orange.download()


def file_def_get():
    orange = FileGet()
    return orange.get_file_list()


def file_create():
    orange = FileGet()
    return orange.mkdir_file_name()


def file_remove():
    orange = FileGet()
    return orange.remove_file()


def file_save():
    orange = FileGet()
    return orange.save_file()