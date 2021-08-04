import datetime


def ogs_runtime(func):
    def wrapper(*args, **kwargs):
        # 装饰器，方法执行前打印执行时间和方法名
        print('%s run func %s' % (datetime.datetime.now(), func.__name__))
        return func(*args, *kwargs)

    return wrapper
