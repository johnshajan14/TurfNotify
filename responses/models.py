from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class Response(models.Model):

    RESPONSE_CHOICES = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    response = models.CharField(
        max_length=3,
        choices=RESPONSE_CHOICES
    )

    reason = models.TextField(
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username} - {self.response}"