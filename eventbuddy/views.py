from django.shortcuts import render
from book.models import Book
from eventbuddy.models import Event

def show_eventbuddy(request):
    events = Event.objects.all()
    context = {
        'events' : events,
    }
    return render(request, "eventbuddy.html", context)
# Create your views here.
