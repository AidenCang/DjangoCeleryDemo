# Django定时任务
# 防止死锁
CELERYD_FORCE_EXECV = True

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

#要验证配置文件是否正常工作且不包含任何语法错误
python -m celeryconfig