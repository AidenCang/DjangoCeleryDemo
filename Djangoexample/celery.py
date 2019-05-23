from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangoexample.settings')
broker = "redis://localhost:6379/1"
app = Celery('Djangoexample', broker=broker)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(lambda: INSTALLED_APPS)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)


app.conf.timezone = 'Asia/Shanghai'
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'test',
        'schedule': 30.0,
        'args': 'Test'
    },
}

#
app.conf.update(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=True,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE={
        'user_task': {
            'task': 'hello.tasks.send_notification',
            'schedule': 30.0,
        },
        # 'login_task': {
        #     'task': 'tasks.login.excute_login_task',
        #     'schedule': timedelta(hours=10),
        # },
    },
    # CELERY_QUEUES=(
    #     Queue('login_queue', exchange=Exchange('login', type='direct'), routing_key='for_login'),
    #     Queue('user_crawler', exchange=Exchange('user_info', type='direct'), routing_key='for_user_info'),
    #     Queue('fans_followers', exchange=Exchange('fans_followers', type='direct'), routing_key='for_fans_followers')
    # )
)
