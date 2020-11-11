from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Food, Meal, MacroGoal


@login_required(login_url='/login')
class MealHomeView(TemplateView):
    template_name = "meals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = datetime.now().strftime('%Y-%m-%d')
        return context


@login_required(login_url='/login')
def date(request, day):
    context = {
        'selected_day': day.strftime('%Y-%m-%d'),
        'today': datetime.now().strftime('%Y-%m-%d'),
        'yesterday': (day + timedelta(days=-1)).strftime('%Y-%m-%d'),
        'tomorrow': (day + timedelta(days=1)).strftime('%Y-%m-%d'),
        'meals': Meal.objects.filter(day_associated=day),
        'goal': MacroGoal.objects.get(start_date__lte=day, end_date__gte=datetime.now())
    }
    return render(request, 'day.html', context)