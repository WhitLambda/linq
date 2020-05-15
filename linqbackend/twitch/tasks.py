from celery.task import periodic_task
from celery.schedules import crontab

# import the twitch api function to run


@periodic_task(run_every=(crontab(minute='*/2')), name='twitch_task_1', ignore_result=True)
def twitch_task_1():

    # just call that function here
