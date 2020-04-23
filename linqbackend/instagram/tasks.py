from celery.task import periodic_task
from celery.schedules import crontab

import datetime
import string
import random

from .models import Comments



@periodic_task(run_every=(crontab(minute='*/1')), name='write_to_db_insta', ignore_result=True)
def write_to_db_insta():
    print("instagram task done :)\n")


# just an example of running a periodic task
# can clean up later