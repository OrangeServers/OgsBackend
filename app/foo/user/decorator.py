from flask import session, redirect
from functools import wraps


def wrapper(func):
    @wraps(func)  # 保存原来函数的所有属性,包括文件名
    def inner(*args, **kwargs):
        # 校验session
        if session.get(""):
            ret = func(*args, **kwargs)  # func = home
            return ret
        else:
            return redirect("/login")

    return inner
