import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

from main.models import Profile
from book.models import Book
from mybuddy.models import OwnedBook

from mybuddy.forms import UpdateForm

@login_required(login_url='main:login')
def show_my_buddy(request):

    form = UpdateForm(request.POST or None)

    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture

    context = {
        'user': user.full_name,
        'profile_picture': profile_picture,
        'form': form
    }
    return render(request, "mybuddy.html", context)

@csrf_exempt
def add_buddy(request):

    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture

    context = {
        'user': user.full_name,
        'profile_picture': profile_picture
    }

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        book = Book.objects.get(pk=data["pk"])
        print(book.title)
        print(book.pk)
        
        new_book = OwnedBook(user=user, owned_book=book, page_track=0, ulasan="", status="W")
        # new_book.save()
        return HttpResponse("ADDED",status=201)
    return render(request, "addbuddy.html", context)

def get_owned_book(request):
    user = Profile.objects.get(user=request.user)
    own_book = list(OwnedBook.objects.filter(user=user))

    data = []

    for buku in own_book:
        buku_asli = Book.objects.get(pk=buku.owned_book.pk)
        each_data = {
            'pk': buku.pk,
            'thumbnail': buku_asli.thumbnail,
            'title': buku_asli.title,
            'description': buku_asli.description,
            'page_count': buku_asli.page_count,
            'page_track': buku.page_track,
            'ulasan': buku.ulasan,
            'status': buku.status,
        }
        if each_data['status'] == 'W':
            each_data['status'] = 'Wishlist'
        elif each_data['status'] == 'F':
            each_data['status'] == 'Finish'
        else:
            each_data['status'] == 'Reading'
        data.append(each_data)

    return HttpResponse(json.dumps(data), content_type="application/json")

