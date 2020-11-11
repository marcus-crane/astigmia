from datetime import datetime

from django.urls import path, register_converter

from . import views


class DateConverter:
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', views.MealHomeView.as_view(), name='meals_index'),
    path('date/<yyyy:day>/', views.date, name='date')
]
