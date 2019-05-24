# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from celery import shared_task
import time


@shared_task(bind=True)
def add(self, x, y):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a + b)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


# We can have either registered task
@task(name='summary')
def send_import_summary():
    print("summary")


# or
@shared_task(bind=True)
def send_notifiction(self):
    print('Here I\’m')

    # Another trick
