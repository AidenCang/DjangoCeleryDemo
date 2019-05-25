from celery.result import ResultBase
from django.http import HttpResponse
from .tasks import add, send_notifiction


def on_raw_message(body):
    print(body)


# Create your views here.
def index(request):
    # print("view.index")
    # result = add.delay(2, 3)
    # send_notifiction.delay()
    # print('===========================')
    # print(result.ready())
    # print(result.get(on_message=on_raw_message, propagate=False))
    from test.apscheduler import scheduler
    # scheduler.remove_all_jobs()
    scheduler.print_jobs()
    return HttpResponse("hello")
