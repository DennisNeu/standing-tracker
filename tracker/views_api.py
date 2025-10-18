# add alongside your measure() view
import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# keep it super simple: in DB we'll just append events
from .models import StateEvent

@csrf_exempt
def state_event(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8"))
        state = data["state"]  # "sitting" or "standing"
        assert state in ("sitting", "standing")
    except Exception as e:
        return JsonResponse({"error": f"bad payload: {e}"}, status=400)

    StateEvent.objects.create(state=state, ts=timezone.now())
    return JsonResponse({"ok": True})
