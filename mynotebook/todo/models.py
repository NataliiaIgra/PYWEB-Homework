from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    ACTIVE = 'A'
    POSTPONED = 'P'
    DONE = 'D'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (POSTPONED, 'Postponed'),
        (DONE, 'Done'),
    ]

    title = models.CharField(max_length=255)
    text = models.TextField(default='', blank=True)
    important = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_now=True, editable=False)
    date_to_complete = models.DateTimeField(default=(datetime.now() + timedelta(days=1)), blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, editable=False)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    def __str__(self):
        return self.title
