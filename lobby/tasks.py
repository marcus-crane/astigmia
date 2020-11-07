from datetime import datetime
from zoneinfo import ZoneInfo

from celery import shared_task
from django.conf import settings

from .auth_backend import retrieve_user_from_api # TODO: This should definitely be pulled out from the auth backend
from .models import User


def get_user_profile():
    return retrieve_user_from_api(username=settings.MV_USERNAME, password=settings.MV_PASSWORD)


@shared_task()
def check_next_session():
    user = User.objects.get(username=settings.MV_USERNAME)
    user_data = get_user_profile() # eww
    session_time = user_data['user']['getprofilemerged']['profile']['nextsession']
    parsed_session_time = datetime.strptime(session_time, '%d/%m/%Y %I:%M:%S %p')
    tzaware_session_time = parsed_session_time.astimezone(ZoneInfo(key='Pacific/Auckland'))
    user.next_session = tzaware_session_time
    user.save()


@shared_task()
def update_targets_and_goals():
    user = User.objects.get(username=settings.MV_USERNAME)
    user_data = get_user_profile()
    user.target_carbs = user_data['user']['getlogin']['sectionfooddiary']['targetcarbohydrate']
    user.target_protein = user_data['user']['getlogin']['sectionfooddiary']['targetprotein']
    user.target_fat = user_data['user']['getlogin']['sectionfooddiary']['targetfat']
    user.current_goals = user_data['user']['getlogin']['sectiongoals']['weeklygoal']
    user.target_weight = user_data['user']['getlogin']['sectiongoals']['targetweight']
    user.current_weight = user_data['user']['getlogin']['sectiongoals']['currentweight']
    user.save()
