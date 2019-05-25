import time

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=1, id='my_job_id')
def test_job():
    time.sleep(4)
    print("I'm a test job!")
    # raise ValueError("Olala!")


register_events(scheduler)


def print_job():
    print("print_job")


def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')
        print(event)


scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.add_job(print_job, trigger='cron', minute='*/5')
scheduler.start()
print("Scheduler started!")
