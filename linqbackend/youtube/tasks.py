from celery.task import periodic_task
from celery.schedules import crontab

from .youtube_api2 import yt_test_func
from .youtube_api2 import main as yt_main_func


@periodic_task(run_every=(crontab(minute='*/2')), name='youtube_task_1', ignore_result=True)
def youtube_task_1():

    # this is the actual function to run
    # yt_main_func()              # getting a """ FileNotFoundError: [Errno 2] No such file or directory: './client_secrets_file.json' """ error

    
    # this is just the test function, can be used for debugging
    yt_test_func()

