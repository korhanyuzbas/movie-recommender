from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class CeleryResult(models.Model):
    PENDING = 1
    COMPLETED = 2
    CANCELLED = 3
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (COMPLETED, 'completed'),
        (CANCELLED, 'cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=300)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
