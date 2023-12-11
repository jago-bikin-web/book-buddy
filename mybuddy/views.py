import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User

from main.models import Profile
from book.models import Book
from mybuddy.models import OwnedBook

from mybuddy.forms import UpdateForm


@csrf_exempt
def update_own_book(request):
    if request.method == "POST":

        form = UpdateForm(request.POST)
        if form.is_valid():
            pk_buku = request.COOKIES.get('book_update')
            buku = OwnedBook.objects.get(pk=pk_buku)
            buku_asli = Book.objects.get(pk=buku.owned_book.pk)

            try:
                page_track = int(request.POST.get('page_track'))
            except ValueError:
                page_track = buku.page_track
            status = request.POST.get('status')
            ulasan = request.POST.get('ulasan')

            if buku_asli.page_count < page_track:
                page_track = buku_asli.page_count
                status = 'F'
            elif page_track <= 0:
                page_track = 0

            if ulasan == "":
                ulasan = buku.ulasan

            buku.page_track = page_track
            buku.status = status
            buku.ulasan = ulasan

            buku.save()

        response = HttpResponse(status=200)
        response.delete_cookie('book_update')
        return response
    return HttpResponseNotFound()


@csrf_exempt
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

    if request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        own_book = OwnedBook.objects.get(pk=data["pk"])

        own_book_data = {
            'page_track': own_book.page_track,
            'status': own_book.status,
            'ulasan': own_book.ulasan,
        }

        response = HttpResponse(json.dumps(
            own_book_data), content_type="application/json")
        response.set_cookie('book_update', own_book.pk)
        return response
    return render(request, "mybuddy.html", context)


@csrf_exempt
@login_required(login_url='main:login')
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

        new_book = OwnedBook(user=user, owned_book=book,
                             page_track=0, ulasan="", status="W")
        new_book.save()
        return HttpResponse("ADDED", status=201)
    return render(request, "addbuddy.html", context)


def get_owned_book(request : HttpResponse):
    username = request.GET.get('username', None)
    if (username == None):
        user = Profile.objects.get(user=request.user)
    else:
        if (username == 'null'):
            return
        user = User.objects.get(username=username)
        user = Profile.objects.get(user=user)
    own_book = list(OwnedBook.objects.filter(user=user))

    data = []

    for buku in own_book:
        buku_asli = Book.objects.get(pk=buku.owned_book.pk)
        each_data = {
            'pk': buku.pk,
            'thumbnail': buku_asli.thumbnail,
            'title': buku_asli.title,
            'authors': buku_asli.authors,
            'description': buku_asli.description,
            'page_count': buku_asli.page_count,
            'page_track': buku.page_track,
            'ulasan': buku.ulasan,
            'status': buku.status,
        }
        if each_data['status'] == 'W':
            each_data['status'] = 'Wishlist'
        elif each_data['status'] == 'F':
            each_data['status'] = 'Finish'
        else:
            each_data['status'] = 'Reading'
        data.append(each_data)

    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def add_page_track(request):
    data = json.loads(request.body.decode("utf-8"))
    buku = OwnedBook.objects.get(pk=data["pk"])
    buku_asli = Book.objects.get(pk=buku.owned_book.pk)

    if buku.page_track < buku_asli.page_count:
        buku.page_track += 1
        buku.save()

    if buku.page_track == buku_asli.page_count:
        buku.status = 'F'
        buku.save()

    return HttpResponse(status=200)


@csrf_exempt
def sub_page_track(request):
    data = json.loads(request.body.decode("utf-8"))
    buku = OwnedBook.objects.get(pk=data["pk"])
    buku_asli = Book.objects.get(pk=buku.owned_book.pk)

    if buku.page_track > 0:
        buku.page_track -= 1
        buku.save()

    if buku.page_track < buku_asli.page_count:
        buku.status = 'R'
        buku.save()

    return HttpResponse(status=200)