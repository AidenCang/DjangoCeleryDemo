from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangoexample.settings')
broker = "redis://localhost:6379/1"
# 自定义队列名称长亮
ROUTE_KEY_VIDEO = "media.video"
ROUTE_KEY_IMAGE = "media.imgage"

# 自定义路由key
QUEUE_NAME_VIDEO = "video"
QUEUE_NAME_IMAGE = "imgage"
##=========================自定义Task的名称======================================
# class MyCelery(Celery):
#
#     def gen_task_name(self, name, module):
#         if module.endswith('.tasks'):
#             module = module[:-6]
#         return super(MyCelery, self).gen_task_name(name, module)
#
# app = MyCelery('main')
##==========================自定义Task的名称=====================================

app = Celery('Djangoexample', broker=broker)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(lambda: INSTALLED_APPS)
app.autodiscover_tasks()


@app.task()
def debug_task():
    print('Request: {0!r}'.format("Request"))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello==='), name='add every 10')

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


@app.task(routing_key=ROUTE_KEY_VIDEO, queue=ROUTE_KEY_IMAGE)
def testcontrib():
    print("testcontrib")


app.conf.timezone = 'Asia/Shanghai'
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'Djangoexample.celery.debug_task',
        'schedule': 5.0,
        'args': ''
    },  # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'Djangoexample.celery.testcontrib',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        # 'schedule': crontab(hour=3, minute=5, ),
        'schedule': crontab(),
        'args': '',
    },
}

app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue(QUEUE_NAME_VIDEO, Exchange('media'), routing_key=ROUTE_KEY_VIDEO),
    Queue(QUEUE_NAME_IMAGE, Exchange('media'), routing_key=ROUTE_KEY_IMAGE),
)

app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
