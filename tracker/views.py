from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.views.decorators.csrf import csrf_exempt

import json

from .models import StandingTime


def standing(request):
    highscore = StandingTime.objects.all().order_by('-time').first() or StandingTime(time=0)
    total = StandingTime.objects.aggregate(Sum('time'))['time__sum'] or 0
    history = get_daily_history_qs()
    print(f"highscore: {highscore.time}; total: {total}")
    return render(request, 'index.html', {'highscore': highscore.time, 'total': total, 'history': history})


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

def get_daily_history_qs():
    return (
        StandingTime.objects.all()
        .annotate(day=TruncDate('created_at'))          # group key
        .values('day')
        .annotate(
            total_seconds=Sum('time'),
            entries=Count('id'),
        )
        .order_by('-day')
    )
