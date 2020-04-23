from celery.task import periodic_task
from celery.schedules import crontab

import datetime
import string
import random

from .models import Comments



@periodic_task(run_every=(crontab(minute='*/1')), name='write_to_db_insta', ignore_result=True)
def write_to_db_insta():
    lettersdigits = string.digits + string.ascii_letters
    u = 'cb_lu_' + ''.join(random.choice(lettersdigits) for i in range(5))
    ms = ''.join(random.choice(lettersdigits) for i in range(15))


    igc_cel_b = Comments.objects.create(
        username = u,
        message = ms,
    )

    print('wrote object {} to the ig_cmts database :) \n'.format(igc_cel_b))


# just an example of running a periodic task
# can clean up later