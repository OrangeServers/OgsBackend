from app.cron.cron import OgsCron


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


def local_cron_close():
    orange = OgsCron()
    return orange.close_job
