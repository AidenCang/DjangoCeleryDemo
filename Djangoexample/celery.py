# -*- coding: UTF-8 -*-
# set the default Django settings module for the 'celery' program.
from __future__ import absolute_import, unicode_literals

import os
import re

from celery import Celery
from celery.schedules import crontab
from .celeryconfig import ROUTE_KEY_VIDEO, ROUTE_KEY_IMAGE, QUEUE_NAME_IMAGE, QUEUE_NAME_VIDEO
from kombu import Queue, Exchange
from .tasks import test

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangoexample.settings')
# 配置消息分发机制
broker = "redis://localhost:6379/1"

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

# 配置路由和消息队列
app.conf.task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue(QUEUE_NAME_VIDEO, Exchange('media'), routing_key=ROUTE_KEY_VIDEO),
    Queue(QUEUE_NAME_IMAGE, Exchange('media'), routing_key=ROUTE_KEY_IMAGE),
)
app.conf.task_routes = ([
                            # 定义Feeds中的路由信息到指定的队列
                            ('feeds.tasks.*', {'queue': 'feeds'}),
                            # 定义hello app中的任务到指定的队列
                            ('hello.tasks.*', {'queue': 'hello'}),
                            (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
                        ],)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'

# 配置时区和定时

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'Djangoexample.tasks.every_30_seconds',
        'schedule': 5.0,
        'args': ''
    },  # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'Djangoexample.tasks.every_monday_morning',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        # 'schedule': crontab(hour=3, minute=5, ),
        'schedule': crontab(),
        'args': '',
    },
}
app.conf.update(
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_annotations={  # 限速
        'Djangoexample.celery.debug_task': {'rate_limit': '10/m'}
    },
    result_expires=3600,
)


# 使用信号机制执行任务
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
