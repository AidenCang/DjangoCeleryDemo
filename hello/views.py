from django.http import HttpResponse
from .tasks import add,send_notifiction


# Create your views here.
def index(request):
    print("view.index")
    result = add.delay(2, 3)
    send_notifiction.delay()
    return HttpResponse("hello")
