import datetime
from django.db import models
from django.contrib.auth.models import User
from datetime import *

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
