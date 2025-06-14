from django.shortcuts import render
from django.http import HttpResponse

def tracker(request):
    return HttpResponse("Hello world! This is the test view of the tracker app. It is used to verify that the app is working correctly. If you see this message, the app is running fine.")
def index(request):
    return HttpResponse("Hello, world. You're at the tracker index. This is the main app of the tracker project. And here the main view will reside.")