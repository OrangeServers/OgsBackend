from app.foo.local.download import DownloadFile
from app.foo.file.file import FileGet


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


def file_rename():
    orange = FileGet()
    return orange.change_file_name()
