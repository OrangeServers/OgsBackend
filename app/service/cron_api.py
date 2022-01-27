from app.cron.cron import OgsCron, CronList
from app.tools.at import ogs_auth_token


@ogs_auth_token
def local_cron_list():
    orange = CronList()
    return orange.cron_list


@ogs_auth_token
def local_cron_auth_list():
    orange = CronList()
    return orange.cron_auth_list


@ogs_auth_token
def local_cron_list_all():
    orange = CronList()
    return orange.cron_list_all


@ogs_auth_token
def local_cron_add():
    orange = OgsCron()
    return orange.add_job()


@ogs_auth_token
def local_cron_pause():
    orange = OgsCron()
    return orange.pause_job()


@ogs_auth_token
def local_cron_resume():
    orange = OgsCron()
    return orange.resume_job()


@ogs_auth_token
def local_cron_del():
    orange = OgsCron()
    return orange.remove_job()


@ogs_auth_token
def local_cron_com_list():
    orange = OgsCron()
    return orange.com_list_job()


@ogs_auth_token
def local_cron_close():
    orange = OgsCron()
    return orange.close_job
