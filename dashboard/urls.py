from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('notifications', views.notifications, name='notifications')
]