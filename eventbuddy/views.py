from django.http import HttpResponse
from django.shortcuts import render
from book.models import Book
from eventbuddy.models import Event
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseRedirect
from eventbuddy.forms import EventForm
from django.urls import reverse

def show_eventbuddy(request):
    events = Event.objects.all()
    context = {
        'events' : events,
    }
    return render(request, "eventbuddy.html", context)

def create_event(request):
    form = EventForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

    context = {'form': form}
    return render(request, "create_event.html", context)

def get_event_json(request):
    events = Event.objects.all()
    return HttpResponse(serializers.serialize('json', events))

# Create your views here.
