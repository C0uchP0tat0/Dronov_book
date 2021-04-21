from django.http import HttpResponse

def index(request) :
    return HttpResponse("Здecь будет выведен список объявлений.") 
