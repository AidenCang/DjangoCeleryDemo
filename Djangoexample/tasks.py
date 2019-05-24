from time import time

from celery import task, bootsteps
import celery
from .celeryconfig import ROUTE_KEY_IMAGE, ROUTE_KEY_VIDEO
from celery.utils.log import get_task_logger
from celery.worker.request import Request

logger = get_task_logger(__name__)


class GlobalRequest(Request):
    # 任务在Worker中执行时会调用该函数
    def on_accepted(self, pid, time_accepted):
        pass

    def on_retry(self, exc_info):
        pass

    def on_success(self, failed__retval__runtime, **kwargs):
        pass

    def on_timeout(self, soft, timeout):
        super(GlobalRequest, self).on_timeout(soft, timeout)
        if not soft:
            logger.warning(
                'A hard timeout was enforced for task %s',
                self.task.name
            )

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super(Request, self).on_failure(
            exc_info,
            send_failed_event=send_failed_event,
            return_ok=return_ok
        )
        logger.warning(
            'Failure detected for task %s',
            self.task.name
        )


class GlobTask(celery.Task):
    request = GlobalRequest
    # 重试时间
    default_retry_delay = 30 * 60
    # 最大重试次数
    max_retries = 10

    # rate_limit =

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # 任务执行失败
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def on_success(self, retval, task_id, args, kwargs):
        # 任务执行成功
        print('{0!r} retval: {1!r} args:{2!r}'.format(task_id, retval, args))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass

    def run(self, *args, **kwargs):
        pass


# class NaiveAuthenticateServer(celery.task):
#     def __init__(self):
#         self.users = {'george': 'password'}
#
#     def run(self):
#         try:
#             pass
#         except KeyError:
#             return False


# 处理数据库类
class DatabaseTask(celery.Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            # self._db = Database.connect()
            pass
        return self._db


class DeadlockDetection(bootsteps.StartStopStep):
    # 自定义消费者
    requires = {'celery.worker.components:Timer'}

    def __init__(self, worker, deadlock_timeout=3600):
        self.timeout = deadlock_timeout
        self.requests = []
        self.tref = None

    def start(self, worker):
        # run every 30 seconds.
        self.tref = worker.timer.call_repeatedly(
            30.0, self.detect, (worker,), priority=10,
        )

    def stop(self, worker):
        if self.tref:
            self.tref.cancel()
            self.tref = None

    def detect(self, worker):
        # update active requests
        for req in worker.active_requests:
            if req.time_start and time() - req.time_start > self.timeout:
                raise SystemExit()

@task(base=DatabaseTask)
def process_rows():
    for row in process_rows.db.table.all():
        # process_row(row)
        pass


@task(base=GlobTask, bind=True)
def every_30_seconds(self):
    logger.info(self.request)
    print('Request: {0!r}'.format(self.request))


@task(base=GlobTask, ignore_result=True)
def test(arg):
    print(arg)


@task(base=GlobTask, routing_key=ROUTE_KEY_VIDEO, queue=ROUTE_KEY_IMAGE)
def every_monday_morning():
    print("testcontrib")
