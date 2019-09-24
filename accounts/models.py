from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followers')
    mileage = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.id}: {self.username}'
