from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Otp(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    otp = models.IntegerField(null = False, blank = False)
    timestamp = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return "otp for %s is %s" % (self.userId, self.otp)

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 30, unique = True, null = False)
    content = models.TextField(max_length = 1000)
    createdOn = models.DateTimeField(default = timezone.now)
    modifiedOn = models.DateTimeField(default = timezone.now)
    bookmark = models.BooleanField(default = False)

    def __str__(self):
        return str(self.title)