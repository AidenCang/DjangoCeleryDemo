CRONJOBS = [
    ('1 * * * *', 'cron.cron.my_scheduled_job', '>> /tmp/scheduled_job.log')
]


def my_scheduled_job():
    print("my_scheduled_job.......")
