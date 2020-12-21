from django.db import models
from django.utils import timezone

class Notes(models.Model):
    title = models.CharField(max_length=30, unique=True, null=False)
    content = models.TextField(max_length=1000)
    createdOn = models.DateTimeField(default=timezone.now)
    modifiedOn = models.DateTimeField(default=timezone.now)
    bookmark = models.BooleanField(default=False)

    def __str__(self):
        return self.title
