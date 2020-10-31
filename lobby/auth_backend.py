from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
import requests

from lobby.models import User


def retrieve_user_from_api(username, password):
    """
    The MyVision API uses integers to reflect the status
    of a request. Here's a few of the ones I've spotted

        4: You must enter both a username and password
        5: Please enter a valid username and password
        10: Successfully performed action
        12: Unexpected field
    """
    url = f'{settings.MV_API_BASE}/proxy/login'
    payload = { 'username': username, 'password': password }
    r = requests.post(url, data=payload)
    data = r.json()
    # TODO: This should make use of `.get` and handle network failure
    if data['res']['status'] == 10:
        return data['data']
    return None


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
                user_data = retrieve_user_from_api(username, password)
                # TODO: This feels a bit dirty so parsing should really happen somewhere else!!
                session_time = user_data['user']['getprofilemerged']['profile']['nextsession']
                parsed_session_time = datetime.strptime(session_time, '%d/%m/%Y %I:%M:%S %p')
                # The API returns a date with no timezone which is nuts?
                # For now I'm just forcing it to my timezone as I'm the only user
                # TODO: This should really be stored as UTC in future
                tzaware_session_time = parsed_session_time.astimezone(ZoneInfo(key='Pacific/Auckland'))
                user = User(
                    username=user_data['user']['username'],
                    first_name=user_data['user']['getprofilemerged']['profile']['firstname'],
                    last_name=user_data['user']['getprofilemerged']['profile']['lastname'],
                    email=user_data['user']['email'],
                    next_session=tzaware_session_time,
                    signed_up=user_data['user']['getprofilemerged']['profile']['startdate'],
                    avatar=user_data['user']['getprofilemerged']['profile']['profileimage'],
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
