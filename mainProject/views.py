from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Hello, myapp1!</h1>')