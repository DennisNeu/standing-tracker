from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def tracker(request):
    return HttpResponse("Hello world! This is the test view of the tracker app. It is used to verify that the app is working correctly. If you see this message, the app is running fine.")
def index(request):
    template = loader.get_template('test.html')
    return HttpResponse(template.render())