from django.db import models

# Create your models here.


class StandingTime(models.Model):
    time = models.DurationField(max_length=20)  # Or use models.DurationField if
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} from {self.start_time} to {self.end_time if self.end_time else 'ongoing'}"
    