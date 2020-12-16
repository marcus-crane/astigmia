import dateutil.parser
from django.conf import settings
import requests

from dashboard.tasks import get_user_profile
from lobby.models import User
from .models import Meal, Food


DAYPART_MAP = {
    'breakfast': 'BR',
    'morningtea': 'MT',
    'lunch': 'LN',
    'afternoontea': 'AT',
    'dinner': 'DN',
    'supper': 'SP'
}


def save_meals_for_week(start_date, end_date):
    # TODO: Use current user ID rather than my own
    token = get_user_profile()['token']
    url = f"{settings.MV_API_BASE}/vision/meal-plan/138516/dates/{start_date}/{end_date}"
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    data = r.json()
    # TODO: Deeeeeep
    if data['res']['status'] == 10:
        mealDays = data['data']['mealPlans']
        if mealDays:
            for dayRecord in mealDays:
                recordDate = dayRecord['date']
                dayParts = dayRecord.get('timings', False)
                if dayParts:
                    for dayPart in dayParts:
                        if dayPart:
                            for meal in dayParts[dayPart]:
                                f, _ = Food.objects.get_or_create(
                                    name=meal.get('title'),
                                    serving_unit='Blah',
                                    serving_size=3.2
                                )
                                m, createdMeal = Meal.objects.get_or_create(
                                    id=meal.get('_id'),
                                    user=User.objects.get(username=settings.MV_USERNAME),
                                    food=f,
                                    time_tracked=dateutil.parser.parser(meal.get('tracked', '2020-02-02')),
                                    day_associated=dateutil.parser.parse(recordDate).date(),
                                    daypart_associated=DAYPART_MAP[dayPart]
                                )
                                if createdMeal:
                                    print(f"Added {meal.get('title')} for {dayPart} on {recordDate}")
