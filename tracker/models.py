from django.db import models

# Create your models here.


class StandingTime(models.Model):
    time = models.FloatField(max_length=20)  # Or use models.DurationField if
    created_at = models.DateTimeField(auto_now_add=True)
