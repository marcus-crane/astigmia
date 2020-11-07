from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Notification


# TODO: Is there middleware to have login_required on every view within a module?
@login_required(login_url='/login')
def index(request):
    current_goals = request.user.current_goals.split('\n')
    return render(request, 'index.html', {'current_goals': current_goals})


@login_required(login_url='/login')
def notifications(request):
    # TODO: Switch to a class based view
    return render(request, 'notifications.html', {'notifications': Notification.objects.all()})
