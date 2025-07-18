from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

import json

from .models import StandingTime


def index(request):
    highscore = StandingTime.objects.all().order_by('-time').first() or StandingTime(time=0)
    total = StandingTime.objects.aggregate(Sum('time'))['time__sum'] or 0
    print(f"highscore: {highscore.time}; total: {total}")
    return render(request, 'index.html', {'highscore': highscore.time, 'total': total})


@csrf_exempt  # Use this decorator to allow POST requests without CSRF token
def save_standing_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            elapsed_time = data.get('elapsed')
            StandingTime.objects.create(time=elapsed_time)

            total = StandingTime.objects.aggregate(Sum('time'))['time__sum'] or 0
            highscore = StandingTime.objects.all().order_by('-time').first()


            return JsonResponse({'status': 'success', 'message': 'Standing time saved successfully', 'total': total, 'highscore': highscore.time})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
