from Flask_App_Settings import app
from app.conf.conf_test import MYSQL_CONF
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

exeutors = {
    "default": ProcessPoolExecutor(max_workers=10)
}

jobstores = {
    'default': SQLAlchemyJobStore(url="mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_CONF['user'],
                                                                              MYSQL_CONF['password'],
                                                                              MYSQL_CONF['host'], MYSQL_CONF['port'],
                                                                              MYSQL_CONF['dbname']))
}
app.scheduler = BackgroundScheduler(exeutors=exeutors, jobstores=jobstores)
scheduler = app.scheduler
