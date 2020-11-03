from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # User metadata
    next_session = models.DateTimeField() # TODO: This should be fetched periodically, could use Celery
    avatar = models.URLField()
    signed_up = models.DateTimeField()

    # Workout targets
    current_goals = models.CharField(max_length=200)
    current_weight = models.FloatField()
    target_weight = models.FloatField()

    # Meal targets
    target_carbs = models.IntegerField()
    target_protein = models.IntegerField()
    target_fat = models.IntegerField()

    def get_remaining_weight(self):
        return round(self.target_weight - self.current_weight, 2)
