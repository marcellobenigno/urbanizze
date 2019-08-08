from django.contrib.auth.models import User
from django.db import models


class Research(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
