# models.py
from datetime import timedelta
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils import timezone


class StandingTimeQuerySet(models.QuerySet):
    def qualifying_days(self, min_seconds=600000):
        return (
            self.annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(total=Sum('time'))
            .filter(total__gt=min_seconds)
            .values_list('day', flat=True)
            .distinct()
        )

    def current_streak(self, min_seconds=600000):
        today = timezone.localdate()
        days = list(self.qualifying_days(min_seconds).order_by('-day'))

        if not days or days[0] < today:
            return 0

        streak = 0
        expected = today
        for d in days:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif d < expected:
                break
        return streak

    def longest_streak(self, min_seconds=600000):
        days = list(self.qualifying_days(min_seconds).order_by('day'))
        if not days:
            return 0

        longest = 0
        current = 0
        prev = None

        for d in days:
            if prev and d == prev + timedelta(days=1):
                current += 1
            else:
                current = 1
            longest = max(longest, current)
            prev = d
        return longest


class StandingTime(models.Model):
    time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = StandingTimeQuerySet.as_manager()

    def __str__(self):
        return f"{self.id}: {self.time} seconds"
