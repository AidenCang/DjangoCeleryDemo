# Celery定时任务设置
CELERY_RESULT_BACKEND = 'django-db'

# 防止死锁
CELERYD_FORCE_EXECV = True

# 配置并发进程数
CELERY_CONCURRENCY = 4

# 设置队列设置多少个子任务就销毁
CELERYD_MAX_TASKS_PER_CHILD = 100


ROUTE_KEY_VIDEO = "media.video"
ROUTE_KEY_IMAGE = "media.imgage"

# 自定义路由key
QUEUE_NAME_VIDEO = "video"
QUEUE_NAME_IMAGE = "imgage"