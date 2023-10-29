from django.http import HttpResponse
from django.shortcuts import render
from book.models import Book
from eventbuddy.models import Event
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponseRedirect
from eventbuddy.forms import EventForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.models import Profile

@login_required(login_url='main:login')
def show_eventbuddy(request):
    events = Event.objects.all()
    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture
    context = {
        'user': user.full_name,
        'profile_picture': profile_picture,
        'events' : events,
    }
    return render(request, "eventbuddy.html", context)

@login_required(login_url='main:login')
def create_event(request):
    form = EventForm(request.POST or None)
    books = Book.objects.all()
    user = Profile.objects.get(user=request.user)
    if user.is_member():
        if form.is_valid() and request.method == "POST":
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

        context = {
            'form': form,
            'books': books,
            }
        return render(request, "create_event.html", context)
    else:
        return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

def get_event_json(request):
    events = Event.objects.all()
    return HttpResponse(serializers.serialize('json', events))

@login_required(login_url='main:login')
def edit_event(request, id):
    # Get product berdasarkan ID
    events = Event.objects.get(pk = id)
    books = Book.objects.all()
    user = Profile.objects.get(user=request.user)

    # Set product sebagai instance dari form
    
    if request.user == events.user and user.is_member():
        form = EventForm(request.POST or None, instance=events)
        if form.is_valid() and request.method == "POST":
            # Simpan form dan kembali ke halaman awal
            form.save()
            return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

        context = {'form': form,
                'books': books,
                }
        return render(request, "edit_event.html", context)
    else:
        return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

@login_required(login_url='main:login')
def delete_event(request, id):
    events = Event.objects.get(pk = id)
    user = Profile.objects.get(user=request.user)
    if request.user == events.user and user.is_member():
        events.delete()
    return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

@login_required(login_url='main:login')
def regis_event(request, id):
    events = Event.objects.get(pk = id)
    if request.user != events.user:
        profile = request.user.profile
        events.participant.add(profile)
    return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))


@login_required(login_url='main:lgin')       
def show_attendees(request, id):
    events = Event.objects.get(pk = id)
    user = Profile.objects.get(user=request.user)
    if request.user == events.user and user.is_member():
        participants = events.participant.all()
        count = participants.count()
        context = {
            'participants': participants,
            'count' : count, 
        }
        return render(request, "attendees.html", context)
    else:
        return HttpResponseRedirect(reverse('eventbuddy:show_eventbuddy'))

# Create your views here.
