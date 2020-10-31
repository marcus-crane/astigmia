from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    next_session = models.DateTimeField()
    avatar = models.URLField()
