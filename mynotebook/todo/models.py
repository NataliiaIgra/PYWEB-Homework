from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(default='', max_length=255, blank=True)  # ???
    text = models.TextField(default='', blank=True)  # ???
    important = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_created=True)  # ???
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    ACTIVE = 'A'
    POSTPONED = 'P'
    DONE = 'D'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (POSTPONED, 'Postponed'),
        (DONE, 'Done'),
    ]

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    def __str__(self):
        return self.title
