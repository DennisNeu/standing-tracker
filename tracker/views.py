from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta
import json

from .models import StandingTime


def index(request):
    highscore = "00 : 01 : 00.00"  # Placeholder for highscore, replace with actual logic if needed
    total = StandingTime.objects.aggregate(Sum('time'))['time__sum'] or 0
    
    return render(request, 'index.html', {'highscore': highscore, 'total': total})


@csrf_exempt  # Use this decorator to allow POST requests without CSRF token
def save_standing_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            elapsed_time = data.get('elapsed')
            StandingTime.objects.create(time=elapsed_time)

            total = StandingTime.objects.aggregate(Sum('time'))['time__sum'] or 0

            return JsonResponse({'status': 'success', 'message': 'Standing time saved successfully', 'total': total})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
