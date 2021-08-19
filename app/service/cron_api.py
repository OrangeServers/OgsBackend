from app.cron.cron import OgsCron, CronList


def local_cron_list():
    orange = CronList()
    return orange.cron_list


def local_cron_auth_list():
    orange = CronList()
    return orange.cron_auth_list


def local_cron_list_all():
    orange = CronList()
    return orange.cron_list_all


def local_cron_add():
    orange = OgsCron()
    return orange.add_job()


def local_cron_pause():
    orange = OgsCron()
    return orange.pause_job()


def local_cron_resume():
    orange = OgsCron()
    return orange.resume_job()


def local_cron_del():
    orange = OgsCron()
    return orange.remove_job()


def local_cron_com_list():
    orange = OgsCron()
    return orange.com_list_job()


def local_cron_close():
    orange = OgsCron()
    return orange.close_job
