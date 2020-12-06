from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    This is an extension of a normal Django user model but with properties
    found within the MV API

    While you could make a User model that inherits all of this metadata
    as a different object, I'd rather it just be part of the user directly

    Similarly, we are dealing with an actual representation of a User after
    all so it makes sense to get all of the methods and fields for free
    such as `get_full_name()` and all that.
    """
    # User metadata
    next_session = models.DateTimeField()
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

    # Meal metadata
    favourited_food = models.ManyToManyField(to='meals.Food', related_name='favourited_by')

    def get_remaining_weight(self):
        return round(self.target_weight - self.current_weight, 2)
