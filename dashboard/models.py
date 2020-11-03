from django.db import models


class Notification(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=40)
    created_at = models.DateTimeField()
    message = models.CharField(max_length=200)
