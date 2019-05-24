# 配置路由器的任务传输格式、结果序列化格式，接受的上下文格式，默认为JSON格式
import re

from kombu import Queue, Exchange

task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = {'pickle'}

# 任务在celery中的表示方法是以下面的路劲来表示
# [tasks]
#   . Djangoexample.celery.debug_task
#   . Djangoexample.celery.test
#   . feeds.tasks.useremail
#   . feeds.tasks.userfeels
#   . hello.tasks.add
#   . hello.tasks.mul
#   . hello.tasks.send_notifiction
#   . hello.tasks.xsum
#   . summary

# 定义默认队列名称
task_default_queue = 'default'

task_routes = ([
                   # 定义Feeds中的路由信息到指定的队列
                   ('feeds.tasks.*', {'queue': 'feeds'}),
                   # 定义hello app中的任务到指定的队列
                   ('hello.tasks.*', {'queue': 'hello'}),
                   (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
               ],)

task_queues = (
    Queue('default', routing_key='task.#'),
    Queue('feed_tasks', routing_key='feed.#'),
)

task_queues = (
    Queue('feed_tasks', routing_key='feed.#'),
    Queue('regular_tasks', routing_key='task.#'),
    Queue('image_tasks', exchange=Exchange('mediatasks', type='direct'),
          routing_key='image.compress'),
)

task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'


# Celery定时任务设置
CELERY_RESULT_BACKEND = 'django-db'

# 防止死锁
CELERYD_FORCE_EXECV = True
