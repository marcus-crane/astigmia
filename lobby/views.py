from django.http import HttpResponse


def index(request):
    # TODO: Stick a proper homepage here
    return HttpResponse("Please take a seat.")
