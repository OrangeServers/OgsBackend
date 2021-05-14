from app.foo.user.AccUser import UserLogin, CheckUser, UserRegister


def acc_login_dl():
    orange = UserLogin()
    return orange.login_dl()


def acc_chk_username():
    orange = CheckUser()
    return orange.check()


def acc_com_register():
    orange = UserRegister()
    return orange.register()
