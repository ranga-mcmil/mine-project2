from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_mine = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    balance = models.CharField(max_length=250)

