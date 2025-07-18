from django.shortcuts import render


def index(request):
    highscore = "00 : 01 : 00.00"  # Placeholder for highscore, replace with actual logic if needed
    return render(request, 'index.html', {'highscore': highscore})
