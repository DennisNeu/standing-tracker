from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the tracker index. This is the main app of the tracker project. And here the main view will reside.")