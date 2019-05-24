# Django异步队列和定时测试项目
本项目主要使用APScheduler、django-contrib、celery实现Django异步队列和定时器操作

## Celery 异步消息队列和定时任务使用

[Celery 安装使用](http://docs.celeryproject.org/en/master/getting-started/first-steps-with-celery.html#choosing-a-broker)

[Django使用celery](http://docs.celeryproject.org/en/master/django/first-steps-with-django.html)

Django Extensions:

[django-celery-results](https://pypi.org/project/django-celery-results/) : Using the Django ORM/Cache as a result backend

[django-celery-beat](https://pypi.org/project/django-celery-beat/) - Database-backed Periodic Tasks with Admin interface

[beat-custom-schedulers](http://docs.celeryproject.org/en/master/userguide/periodic-tasks.html#beat-custom-schedulers) : 还有django-celery-beat扩展，它将计划存储在Django数据库中，并提供了一个方便的管理界面来管理运行时的周期性任务。

[DJANGO_SETTINGS_MODULE](https://django.readthedocs.io/en/latest/topics/settings.html#envvar-DJANGO_SETTINGS_MODULE)

    选择并安装消息传输（代理）。
    RabbitMQ/Redis/Amazon SQS
    安装Celery并创建您的第一个任务。
    启动worker并调用任务。
    在任务过渡到不同状态时跟踪任务，并检查返回值


## CeleryDjango配置

    (venv) ➜  Djangoexample git:(master) ✗ tree -L 2
    .
    ├── Djangoexample
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── celery.py #1.新建一个celery文件，配置一个全局的celery，
    │   ├── celeryConf.py
    │   ├── celeryconfig.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── README.md
    ├── __pycache__
    │   └── manage.cpython-37.pyc
    ├── blog
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tasks.py
    │   ├── tests.py
    │   └── views.py
    ├── celerybeat-schedule
    ├── db.sqlite3
    ├── feeds
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tasks.py
    │   ├── tests.py
    │   └── views.py
    ├── hello
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tasks.py
    │   ├── tests.py
    │   └── views.py
    ├── manage.py
    ├── requirements.txt
    ├── templates
    ├── test
    │   ├── __init__.py
    │   └── apscheduler.py
    └── venv
        ├── bin
        ├── include
        ├── lib
        └── pyvenv.cfg
    
    18 directories, 37 files

1.在Djangoexample中新建一个文件celery.py配置celery的默认信息

2.在Djangoexample中配置一下信息，在Django启动的时候自动加载（1）中设置的参数

    from __future__ import absolute_import, unicode_literals
    
    # This will make sure the app is always imported when
    # Django starts so that shared_task will use this app.
    from .celery import app as celery_app
    
    __all__ = ('celery_app',)
3.在每一个app的__init__.py文件中配置，celery在加载文件是可以查找到当前应用下的任务

    default_app_config = 'hello.apps.HelloConfig'
    
4.`requirements.txt`中保存了项目依赖的包

    pip install -r requirements.txt

5.配置相关的app

    INSTALLED_APPS = [
        .....
        'django_celery_results',
        'django_celery_beat',
        'hello.apps.HelloConfig',
        'feeds.apps.FeelsConfig',
        'blog.apps.BlogConfig',
        ....
    ]



# 进程管理工具

    pip install supervisor
    从定向配置文件
    echo_supervisord_conf > conf/supervisord.conf


# 将错误的任务路由到专用队列：
task_routes = {
    'tasks.add': 'low-priority',
}

# 对任务进行速率限制(每分钟十个)
task_annotations = {
    'tasks.add': {'rate_limit': '10/m'}
}

# 在启动是限速
celery -A tasks control rate_limit tasks.add 10/m


# 远程控制命令以及如何监视工作人员正在执行的操作的详细信息

