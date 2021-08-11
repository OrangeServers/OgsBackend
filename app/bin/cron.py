import time
from Flask_App_Settings import app
import psutil, os, signal
from datetime import datetime, date
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

exeutors = {
    "default": ProcessPoolExecutor(max_workers=10)
}
app.scheduler = BackgroundScheduler(exeutors=exeutors)


def job(text):
    print(text)
    print(psutil.virtual_memory())
    print(os.getpid(), os.getppid())


def aps_run():
    # cnres = ConnRedis(REDIS_CONF['host'], REDIS_CONF['port'])
    # cnres.set_red('cron1_pid', os.getpid())
    # scheduler = BlockingScheduler()
    # scheduler = BackgroundScheduler()
    # 在特定时间周期性的触发 也就是cron 每天的14-15点 隔1分运行一次，不加*则就在指定点运行一次
    app.scheduler.add_job(job, 'cron', hour='10-15', minute='*/1', args=['test'])
    app.scheduler.start()

    # try:
    #     while True:
    #         time.sleep(2)
    #         print('sleep')
    # except (KeyboardInterrupt, SystemExit):
    #     # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #     scheduler.shutdown()
    #     print('Exit The Job!')


def print_test(param):
    print("姓名：{}".format(param))


# 动态启动定时任务
@app.route('/start')
def start():
    # 5.启动调度器，不阻塞
    app.scheduler.start()
    return '启动成功'


# 动态添加定时任务
@app.route("/add_job/<param>")
def add_job(param):
    app.scheduler.add_job(print_test, 'interval', seconds=3, args=[param], id=param)
    return "动态添加定时任务：{}".format(param)


# 动态暂停定时任务
@app.route("/pause_job/<param>")
def pause_job(param):
    app.scheduler.pause_job(param)
    return "动态暂停定时任务成功：{}".format(param)


# 动态恢复定时任务
@app.route("/resume_job/<param>")
def resume_job(param):
    app.scheduler.resume_job(param)
    return "动态恢复定时任务成功：{}".format(param)


# 动态删除定时任务
@app.route("/remove_job/<param>")
def remove_job(param):
    app.scheduler.remove_job(param)
    return "动态删除定时任务成功：{}".format(param)


# 关闭所有定时任务
@app.route("/shoutdown")
def close_job():
    app.scheduler.shutdown()
    return "关闭所有定时任务成功"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=28110)
    # aps_run()
