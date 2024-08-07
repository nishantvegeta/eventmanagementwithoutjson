from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    location = models.CharField(max_length=40, default='Unknown')
    total_participants = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    image = models.ImageField(upload_to='event_images/', default='default.jpg')

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} booked {self.event.title}'

        