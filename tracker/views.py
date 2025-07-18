from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import StandingTime


def index(request):
    highscore = "00 : 01 : 00.00"  # Placeholder for highscore, replace with actual logic if needed
    return render(request, 'index.html', {'highscore': highscore})

def save_standing_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            elapsed_time = data.get('standing_time', '00:00:00.00')
            StandingTime.objects.create(time=elapsed_time)
            return JsonResponse({'status': 'success', 'message': 'Standing time saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
