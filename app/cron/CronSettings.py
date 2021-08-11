from Flask_App_Settings import app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

exeutors = {
    "default": ProcessPoolExecutor(max_workers=10)
}
app.scheduler = BackgroundScheduler(exeutors=exeutors)
scheduler = app.scheduler
