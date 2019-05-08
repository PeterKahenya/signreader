from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request,"home.html",None,None)
@csrf_exempt
def api(request):
    print(request.POST)
    return HttpResponse("api response")