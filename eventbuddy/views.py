from django.http import HttpResponse, HttpResponseNotFound
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
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='main:login')
def show_eventbuddy(request):
    events = Event.objects.all()
    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture
    form = EventForm(request.POST or None)
    books = Book.objects.all()
    context = {
        'user': user.full_name,
        'profile_picture': profile_picture,
        'events' : events,
        'form': form,
        'books': books,
    }
    return render(request, "ebuddy.html", context)

@login_required(login_url='main:login')
def create_event(request):
    form = EventForm(request.POST or None)
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if user.is_member():
            if form.is_valid():
                event = form.save(commit=False)
                event.user = request.user
                event.save()
                return HttpResponse(b"CREATED", status=201)

        else:
            return HttpResponseNotFound()

@login_required(login_url='main:login')
def get_event_json(request):
    events = Event.objects.all()
    return HttpResponse(serializers.serialize('json', events))

@login_required(login_url='main:login')
def get_book_json(request, id):
    book = Book.objects.get(pk = id)
    return HttpResponse(serializers.serialize('json', [book]))

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


@login_required(login_url='main:login')       
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
    

@csrf_exempt
def add_event_ajax(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            date = form.cleaned_data["date"]
            description = form.cleaned_data["description"]
            user = request.user
            book = form.cleaned_data["book"]

            new_event = Event(book=book, user=user, name=name, date=date, description=description)
            new_event.save()

            return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()
# Create your views here.
