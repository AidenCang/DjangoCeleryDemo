from celery import task, current_task, shared_task


@shared_task()
def userfeels():
    print("用户反馈")


@shared_task()
def useremail():
    print("发送用户邮件")
