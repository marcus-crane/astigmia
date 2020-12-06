from datetime import datetime
from zoneinfo import ZoneInfo

from celery import shared_task
from django.conf import settings
import requests

from lobby.auth_backend import retrieve_user_from_api  # TODO: This should definitely be extracted from the auth backend
from lobby.models import User

from .models import Notification


def get_user_profile():
    return retrieve_user_from_api(username=settings.MV_USERNAME, password=settings.MV_PASSWORD)


@shared_task()
def check_next_session():
    user = User.objects.get(username=settings.MV_USERNAME)
    user_data = get_user_profile() # eww
    session_time = user_data['user']['getprofilemerged']['profile']['nextsession']  # TODO: Should be using `.get`
    parsed_session_time = datetime.strptime(session_time, '%d/%m/%Y %I:%M:%S %p')
    tzaware_session_time = parsed_session_time.astimezone(ZoneInfo(key='Pacific/Auckland'))
    user.next_session = tzaware_session_time
    user.save()


@shared_task()
def update_targets_and_goals():
    user = User.objects.get(username=settings.MV_USERNAME)
    user_data = get_user_profile()
    # TODO: Surely there's some sort of shorthand that can be used instead
    user.target_carbs = user_data['user']['getlogin']['sectionfooddiary']['targetcarbohydrate']
    user.target_protein = user_data['user']['getlogin']['sectionfooddiary']['targetprotein']
    user.target_fat = user_data['user']['getlogin']['sectionfooddiary']['targetfat']
    user.current_goals = user_data['user']['getlogin']['sectiongoals']['weeklygoal']
    user.target_weight = user_data['user']['getlogin']['sectiongoals']['targetweight']
    user.current_weight = user_data['user']['getlogin']['sectiongoals']['currentweight']
    user.save()


# TODO: Move all of this stuff into its own API client rather than exposing the externals inside the task module
def retrieve_notifications_from_api(token, user_id, page=1):
    """
    The MyVision API uses integers to reflect the status
    of a request. Here's a few of the ones I've spotted

        4: You must enter both a username and password
        5: Please enter a valid username and password
        10: Successfully performed action
        12: Unexpected field
    """
    url = f'{settings.MV_API_BASE}/notification/{user_id}?page={page}'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    data = r.json()
    # TODO: This should make use of `.get` and handle network failure
    if int(data['res']['success']) == 10:
        return data['data']['notifications']
    return None


def save_notifications(token, user_id, page):
    response = retrieve_notifications_from_api(token, user_id, page)
    if not len(response['docs']):
        return False
    for notification in response['docs']:
        Notification.objects.get_or_create(
            id=notification.get('_id'),
            message=notification.get('message'),
            created_at=datetime.strptime(
                # TODO: Timezone parsing should be done client side (although this is only an NZ/AUS gym so...
                notification.get('created_at'), '%Y-%m-%dT%H:%M:%S.%fZ').astimezone(ZoneInfo(key='Pacific/Auckland')
            )
        )
    if response['hasNextPage']:
        save_notifications(token, user_id, page=page+1)


@shared_task()
def fetch_notifications():
    # TODO: Persist token somewhere either in memory or in eg; redis/rabbitmq
    token = get_user_profile()['token']
    # TODO: User ID shouldn't be hardcoded but it works for now
    save_notifications(token, user_id=138516, page=1)


