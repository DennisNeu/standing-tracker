from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import StandingTime
from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta


def index(request):
    highscore = "00 : 01 : 00.00"  # Placeholder for highscore, replace with actual logic if needed
    return render(request, 'index.html', {'highscore': highscore})

@csrf_exempt  # Use this decorator to allow POST requests without CSRF token
def save_standing_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            elapsed_time = data.get('elapsed')
            StandingTime.objects.create(time=timedelta(seconds=elapsed_time))
            return JsonResponse({'status': 'success', 'message': 'Standing time saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
