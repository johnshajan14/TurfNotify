from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    title = models.CharField(max_length=100)

    event_date = models.DateField()

    event_time = models.TimeField()

    location = models.CharField(max_length=200)

    max_players = models.PositiveIntegerField(
        default=10
    )

    announcement = models.TextField(
        blank=True,
        default=""
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title