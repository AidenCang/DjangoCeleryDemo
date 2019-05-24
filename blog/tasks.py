from akismet import Akismet
from celery import Task
from celery import task
from celery.utils.log import get_task_logger
from celery.worker.request import Request
from django.core.exceptions import ImproperlyConfigured

from Djangoexample import settings
from blog.models import Comment

# from django.contrib.sites.models import Site

logger = get_task_logger(__name__)


class MyRequest(Request):
    'A minimal custom request to log failures and hard time limits.'

    def on_timeout(self, soft, timeout):
        super(MyRequest, self).on_timeout(soft, timeout)
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


class MyTask(Task):
    """
    :keyword 定义任务基类
    """
    # 定义work请求类
    request = MyRequest

    def run(self, *args, **kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        pass


@task(base=MyTask, serializer='json', name="blog.task.filter_comment", default_retry_delay=30 * 60,
      retry_backoff=True)  # 30分钟
def spam_filter(comment_id, remote_addr=None):
    # 获取日志
    logger = spam_filter.get_logger()
    logger.info('Running spam filter for comment %s', comment_id)

    comment = Comment.objects.get(pk=comment_id)
    # current_domain = Site.objects.get_current().domain
    # 垃圾留言过滤系统
    akismet = Akismet(settings.AKISMET_KEY, 'http://{0}'.format(''))
    if not akismet.verify_key():
        raise ImproperlyConfigured('Invalid AKISMET_KEY')

    is_spam = akismet.comment_check(user_ip=remote_addr,
                                    comment_content=comment.comment,
                                    comment_author=comment.name,
                                    comment_author_email=comment.email_address)
    if is_spam:
        comment.is_spam = True
        comment.save()

    return is_spam


@task(ignore_result=True)
def blogTask():
    pass

# 60秒后执行
# blogTask.delay(retry=True, retry_policy={
#     'max_retries': 3,
#     'interval_start': 0,
#     'interval_step': 0.2,
#     'interval_max': 0.2,
# })
