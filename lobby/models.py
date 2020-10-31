from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # User metadata
    next_session = models.DateTimeField() # TODO: This should be fetched periodically, could use Celery
    avatar = models.URLField()
    signed_up = models.DateTimeField()

    # Workout targets
    current_goal = models.TextField()
    current_weight = models.FloatField()
    target_weight = models.IntegerField()

    # Meal targets
    target_carbs = models.IntegerField()
    target_protein = models.IntegerField()
    target_fat = models.IntegerField()
