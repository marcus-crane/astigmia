from django.db import models


class Notification(models.Model):
    """
    Each notification in the MV API already has its own unique
    ID so we can just reuse that instead. We'll need to store
    it anyway in order to issue a DELETE request.

    TODO: I believe the ID is static at only about ~30 characters
    in length but I'd have to check that for sure
    """
    id = models.CharField(primary_key=True, editable=False, max_length=40)
    created_at = models.DateTimeField()
    message = models.CharField(max_length=200)
