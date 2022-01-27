from app.foo.local.download import DownloadFile
from app.foo.file.file import FileGet
from app.tools.at import ogs_auth_token


@ogs_auth_token
def file_download():
    orange = DownloadFile()
    return orange.download()


@ogs_auth_token
def file_def_get():
    orange = FileGet()
    return orange.get_file_list()


@ogs_auth_token
def file_create():
    orange = FileGet()
    return orange.mkdir_file_name()


@ogs_auth_token
def file_remove():
    orange = FileGet()
    return orange.remove_file()


@ogs_auth_token
def file_save():
    orange = FileGet()
    return orange.save_file()


@ogs_auth_token
def file_rename():
    orange = FileGet()
    return orange.change_file_name()


@ogs_auth_token
def file_size():
    orange = FileGet()
    return orange.get_file_size()
