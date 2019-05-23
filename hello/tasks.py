# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from celery import shared_task
import time


@shared_task
def add(x, y):
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
@shared_task
def send_notifiction():
    print('Here I\’m')
    # Another trick
