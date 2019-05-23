# from apscheduler.scheduler import Scheduler
# import random
#
# from apscheduler.schedulers
# from django.core.cache import cache
# # 实例化
# sched = Scheduler()
#
# # 每30秒执行一次
# @sched.interval_schedule(seconds=30)
# def sched_test():
#     """
#     测试-定时将随机数保存到redis中
#     :return:
#     """
#     seed = "123456789"
#     sa = []
#     for i in range(4):
#         sa.append(random.choice(seed))
#     code = ''.join(sa)
#     cache.set("test_"+code, code)