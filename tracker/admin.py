from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StandingTime  # whatever models you want

admin.site.register(StandingTime)
