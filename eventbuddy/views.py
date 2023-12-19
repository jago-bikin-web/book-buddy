import json
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
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
from django.contrib.auth.models import User


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
        
def show_json(request):
    data = Event.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@csrf_exempt
def create_event_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        book_pk = data.get("pkBook")
        book = Book.objects.get(pk = book_pk)

        events = Event.objects.all()

        for e in events:
            already_book = Book.objects.get(pk=e.book.pk)
            if already_book.title == book.title:
                return JsonResponse({"status": False}, status=401)

        user = data.get("username")
        user = User.objects.get(username = user)
        name = data.get("name")
        date = data.get("date")
        description = data.get("description")


        new_event = Event.objects.create(
            user=user,
            book=book,
            name=name,
            date=date,
            description=description,
        )

        new_event.save()

        return JsonResponse({"status": True}, status=200)
    else:
        return JsonResponse({"status": False}, status=401)

@csrf_exempt
def regis_flutter(request):
    if request.method == "POST":
        data = json.loads(request.body)

        event_pk = data.get("id")
        events = Event.objects.get(pk = event_pk)
        user = data.get("username")
        user = User.objects.get(username = user)
        profile = request.user.profile

        if request.user != events.user:
            if events.participant.filter(pk=profile.pk).exists():
                return JsonResponse({"status": 1}, status=401)
            else:
                events.participant.add(profile)
                return JsonResponse({"status": 2}, status=200)
        else:
            return JsonResponse({"status": 3}, status=401)

def get_event_flutter(request):
    events = Event.objects.all()
    list_event = []

    for e in events:
        book = Book.objects.get(pk=e.book.pk)
        user_event = Profile.objects.get(user=e.user)
        
        participants_list = []
        for participant in e.participant.all():
            participant_item = {
                "participant_name": participant.full_name,
                # tambahkan atribut lain sesuai kebutuhan
            }
            participants_list.append(participant_item)

        event_item = {
            "event_pk": e.pk, 
            "book_thumbnail": book.thumbnail,
            "event_name": e.name,
            "event_description": e.description,
            "event_date": e.date.strftime("%Y-%m-%d"),
            "event_user_fullname": user_event.full_name,
            "event_username": user_event.user.username,
            "event_participants": participants_list,
        }
        list_event.append(event_item)

    return JsonResponse(list_event, safe=False)

@csrf_exempt
def delete_flutter(request):
    if request.method == "POST":
        data = json.loads(request.body)

        event_pk = data.get("id")
        events = Event.objects.get(pk = event_pk)
        user_name = data.get("username")
        user = User.objects.get(username = user_name)

        if user == events.user:
            events.delete()
        return JsonResponse({"status": True}, status=200)
    else:
        return JsonResponse({"status": False}, status=401)