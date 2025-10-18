# tracker/utils.py
from datetime import datetime, timedelta
from collections import defaultdict
from django.utils import timezone
from django.db.models import Q
from .models import StateEvent

def standing_seconds_by_day(start: datetime, end: datetime):
    """
    Return {date: seconds_standing} for [start, end).
    start/end should be aware datetimes in your local tz.
    """
    assert start.tzinfo is not None and end.tzinfo is not None, "Use aware datetimes"
    assert start < end

    # 1) What was the state right before 'start'?
    prev = (
        StateEvent.objects
        .filter(ts__lt=start)
        .order_by("-ts")
        .first()
    )
    current_state = prev.state if prev else "sitting"   # default if no history

    # 2) Pull all events in [start, end)
    events = list(
        StateEvent.objects
        .filter(ts__gte=start, ts__lt=end)
        .order_by("ts")
        .values_list("ts", "state")
    )

    # 3) Walk the timeline, summing standing durations and splitting by day
    totals = defaultdict(int)  # {date: seconds}
    cursor = start

    def add_span(span_start, span_end, standing: bool):
        if not standing or span_end <= span_start:
            return
        # split over days
        s = span_start
        while s < span_end:
            day_end = (s.replace(hour=0, minute=0, second=0, microsecond=0)
                        + timedelta(days=1))
            chunk_end = min(day_end, span_end)
            day_key = s.date()
            totals[day_key] += int((chunk_end - s).total_seconds())
            s = chunk_end

    for ts, state in events:
        add_span(cursor, ts, current_state == "standing")
        current_state = state
        cursor = ts

    # tail from last event to 'end'
    add_span(cursor, end, current_state == "standing")

    return dict(totals)

def standing_minutes_by_day(start: datetime, end: datetime):
    secs = standing_seconds_by_day(start, end)
    # round to whole minutes for display
    return {d: round(s/60) for d, s in secs.items()}
