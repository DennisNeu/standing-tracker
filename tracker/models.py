from django.db import models

# Create your models here.


class Session(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.session_id} from {self.start_time} to {self.end_time if self.end_time else 'ongoing'}"
    