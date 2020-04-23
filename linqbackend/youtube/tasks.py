from celery.task import periodic_task
from celery.schedules import crontab


@periodic_task(run_every=(crontab(minute='*/2')), name='youtube_task_1', ignore_result=True)
def youtube_task_1():
    # run every 30 minutes
    # do something here
    print("youtube task done :)\n")
