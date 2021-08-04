import datetime, functools
from enum import Enum, unique


@unique
class Filepath(Enum):
    # 枚举类，定义常量
    Image_path = '/data/putfile/'
    File_path = '/data/tmp/test'


def ogs_runtime_test(func):
    def wrapper(*args, **kwargs):
        # 不带参数的装饰器，方法执行前打印执行时间和方法名
        print('%s run func %s text %s' % (datetime.datetime.now(), func.__name__))
        return func(*args, *kwargs)
    return wrapper


def ogs_runtime(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 带参数的装饰器，方法执行前打印执行时间和方法名
            pth = Filepath.File_path.value
            print('%s run func %s text %s %s' % (datetime.datetime.now(), func.__name__, text, pth))
            return func(*args, *kwargs)
        return wrapper
    return decorator