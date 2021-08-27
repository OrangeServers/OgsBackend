import datetime, functools, logging
from logging import handlers
from enum import Enum, unique
from flask import request
from app.tools.SqlListTool import ListTool
from app.sqldb.SqlAlchemyDB import t_acc_user, t_auth_host


def auth_list_get():
    lt = ListTool()
    name = request.values.get('name')
    grp_name = t_acc_user.query.filter_by(name=name).first()
    que_auth_group = t_auth_host.query.filter(t_auth_host.user.like("%{}%".format(name))).all()
    que_grp_group = t_auth_host.query.filter(t_auth_host.user_group.like("%{}%".format(grp_name.group))).all()
    auth_list = set(list(lt.auth_ls_list_que(que_auth_group)) + list(lt.auth_ls_list_que(que_grp_group)))
    return auth_list


def ogs_runtime_test(func):
    def wrapper(*args, **kwargs):
        # 不带参数的装饰器，方法执行前打印执行时间和方法名
        print('%s run func text %s' % (datetime.datetime.now(), func.__name__))
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


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, level='info', when='D', backCount=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger('/data/logs/ogsbackend.log')
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        self.sh = logging.StreamHandler()  # 往屏幕上输出
        self.sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        self.th = handlers.TimedRotatingFileHandler(filename='/data/logs/ogsbackend.log', when=when,
                                                    backupCount=backCount,
                                                    encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        self.th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(self.sh)  # 把对象加到logger里
        self.logger.addHandler(self.th)


Log = Logger()


@unique
class Filepath(Enum):
    # 枚举类，定义常量
    Image_path = '/data/putfile/'
    File_path = '/data/tmp/test'
