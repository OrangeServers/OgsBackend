from app.foo.user.user import UserLogin, CheckUser, UserRegister, UserLogin2, UserLogout
from app.tools.at import ogs_auth_token


def acc_login_dl():
    orange = UserLogin()
    return orange.login_dl()


def acc_chk_username():
    orange = CheckUser()
    return orange.check()


def acc_com_register():
    orange = UserRegister()
    return orange.register()


def acc_login_dl2():
    orange = UserLogin2()
    return orange.login_dl()


def acc_login_out():
    orange = UserLogout()
    return orange.logout()
