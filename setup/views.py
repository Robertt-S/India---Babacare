#from django.http import HttpResponse
from django.shortcuts import render



#responses when the pages are requested
def homepage(request):
    #return HttpResponse('Hello World! I\'m home')
    return render(request, 'home.html')

def about(request):
    #return HttpResponse('My about page')
    return render(request, 'about.html')