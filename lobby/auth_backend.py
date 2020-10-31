from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from lobby.models import User


class MyVisionBackend(BaseBackend):
    """
    Authenticates against the MyVision backend, as if it were
    any old Django backend

    This ensures that while we handle users locally, we don't
    have to worry about storing anything but the access token

    We can throw away the username and password as it's only
    used for logging in

    Similarly, we can mostly discard user profile information
    as we store it against the equivalent Django user object
    """

    def authenticate(self, request, username=None, password=None):
        """
        The MyVision API supports two types of logins:
            - Username + password (initial login)
            - Token (subsequent logins)

        For now, we'll just store the username and password
        as a static variable in the base `settings.py`
        given I'm the only user

        We'll still send the username and password to the
        MyVision API in order to get an access token

        For the duration of the session, we'll use that
        access token instead but in future, it might
        be preferable to log back in using an access
        token

        Let's not get ahead of ourselves though...
        """
        login_valid = (settings.MV_USERNAME == username)
        password_valid = (settings.MV_PASSWORD == password)
        if login_valid and password_valid:
            try:
                user = get_user_model().objects.get(username=username)
            except User.DoesNotExist:
                user = User(
                    username=username
                )
                user.save()
            return user
        return None

    def get_user(self, user_id):
        """
        At the moment, having the ability to fetch
        other users is a little redundant, being
        the only user myself but technically a
        personal trainer is just another user so
        down the line, that would likely be a
        user case

        In the API, your PT is just represented
        as text rather than a user object but
        I'd prefer to store them as the user
        that they are
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
