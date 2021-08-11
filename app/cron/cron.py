import time
from flask import request, jsonify
import psutil, os, signal
from datetime import datetime, date
from app.cron.CronSettings import scheduler, app


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
    scheduler.add_job(job, 'cron', hour='10-15', minute='*/1', args=['test'], id='1')
    scheduler.start()

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
    scheduler.start()
    return '启动成功'


# 动态添加定时任务2  对现有项目定制。。。。。
@app.route("/add_job/")
def add_job2(param):
    job_minute = request.values.get('job_minute')
    job_hour = request.values.get('job_hour')
    job_day = request.values.get('day')
    job_month = request.values.get('job_month')
    job_week = request.values.get('week')
    scheduler.add_job(job, 'cron', week=job_week, month=job_month, day=job_day, hour=job_hour, minute=job_minute,
                      id='1')
    return "动态添加定时任务：{}".format(param)


# 动态添加定时任务
@app.route("/add_job/<param>")
def add_job(param):
    scheduler.add_job(print_test, 'interval', seconds=3, args=[param], id=param)
    return "动态添加定时任务：{}".format(param)


# 动态暂停定时任务
@app.route("/pause_job/<param>")
def pause_job(param):
    scheduler.pause_job(param)
    return "动态暂停定时任务成功：{}".format(param)


# 动态恢复定时任务
@app.route("/resume_job/<param>")
def resume_job(param):
    scheduler.resume_job(param)
    return "动态恢复定时任务成功：{}".format(param)


# 动态删除定时任务
@app.route("/remove_job/<param>")
def remove_job(param):
    scheduler.remove_job(param)
    return "动态删除定时任务成功：{}".format(param)


# 关闭所有定时任务
@app.route("/shoutdown")
def close_job():
    scheduler.shutdown()
    return "关闭所有定时任务成功"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=28110)
    # aps_run()
