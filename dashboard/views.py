from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login')
def index(request):
    current_goals = request.user.current_goals.split('\n')
    return render(request, 'index.html', {'current_goals': current_goals})
