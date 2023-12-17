import json
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from reachbuddy.models import Thread
from main.models import Profile
from book.models import Book
from reachbuddy.forms import ThreadForm
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url='main:login')
def show_reachbuddy(request):
    threads = Thread.objects.all()

    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture

    context = {
        'user': user.full_name,
        'profile_picture': profile_picture,
        'threads': threads
    }

    return render(request, "reachbuddy.html", context)

@csrf_exempt
@login_required(login_url='main:login')
def create_thread(request):
    form = ThreadForm(request.POST or None)
    books = Book.objects.all()

    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('reachbuddy:show_reachbuddy'))

    context = {
        'form': form,
        'books': books,
        'profile_picture': profile_picture

    }
    return render(request, "create_thread.html", context)

def show_json(request):
    data = Thread.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_book(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_user(request):
    data = User.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_user_id(request, id):
    data = User.objects.get(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def trash_thread(request, id):
    thread = Thread.objects.get(id=id)
    thread.delete()

    response = HttpResponseRedirect(reverse("reachbuddy:show_reachbuddy"))
    return response

def get_books_json(request):
    all_books = Book.objects.all()
    return HttpResponse(serializers.serialize('json', all_books))

def get_profile_json_id(request, id):
    user = User.objects.get(pk=id)
    profile_user = Profile.objects.get(user=user)
    return HttpResponse(serializers.serialize('json', [profile_user]))

def get_book_json_id(request, id):
    chosen_book = Book.objects.get(pk=id)
    return HttpResponse(serializers.serialize('json', [chosen_book]))

def get_threads_json(request):
    all_threads = Thread.objects.all()
    return HttpResponse(serializers.serialize('json', all_threads))

def get_book_json_id_flutter(request, id):
    chosen_book = Book.objects.get(pk=id)
    return HttpResponse(serializers.serialize('json', [chosen_book]))

def get_threads_flutter(request):
    threads = Thread.objects.all()
    threads_posts = []

    for thread in threads:
        book = Book.objects.get(id=thread.book.pk)
        user_profile = Profile.objects.get(user=thread.user)
        
        thread_item = {
            'book_id': book.pk,
            'book_title': book.title,
            'book_image': book.thumbnail,
            'book_author': book.authors,
            'book_published': book.published_date,
            'book_page': book.page_count,

            'profile_image': user_profile.profile_picture,
            'profile_name': thread.user.username,
            'date': thread.date_added,
            'review': thread.review,
            'likes': thread.likes,
        }
        threads_posts.append(thread_item)

    return JsonResponse(threads_posts, safe=False)

def get_thread_detail_flutter(request, id):
    thread = Thread.objects.get(pk=id)

    book = Book.objects.get(id=thread.book.pk)
    user_profile = Profile.objects.get(user=thread.user)
    
    thread_item = {
        'book_title': book.title,
        'book_image': book.thumbnail,
        'book_author': book.authors,
        'book_published': book.published_date,
        'book_page': book.page_count,

        'profile_image': user_profile.profile_picture,
        'profile_name': thread.user.username,
        'date': thread.date_added,
        'review': thread.review,
        'likes': thread.likes,
    }

    return JsonResponse(thread_item, safe=False)

# def get_book_json_by_id(request, book_id):
#     try:
#         chosen_book = Book.objects.get(book_id=book_id)
#         # If you expect multiple books with the same book_id, use filter() instead of get()
#         # chosen_books = Book.objects.filter(book_id=book_id)
#         return HttpResponse(serializers.serialize('json', [chosen_book]))
#     except Book.DoesNotExist:
#         return HttpResponse(status=404)

@csrf_exempt
def create_thread_ajax(request, id):
    form = ThreadForm(request.POST or None)
    user = Profile.objects.get(user=request.user)

    if form.is_valid() and request.method == "POST":
        chosen_book = Book.objects.get(pk=id)
        new_thread = form.save(commit=False)
        new_thread.book = chosen_book
        new_thread.user = request.user
        
        new_thread.save()

        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

@csrf_exempt
def delete_thread_ajax(request, id):
    if request.method == 'DELETE':
        thread = Thread.objects.get(pk=id)
        thread.delete()
        return HttpResponse(b"DELETED", status=200)
    
    return HttpResponseNotFound()

@csrf_exempt
def create_thread_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        book_pk = data.get("pkBook")
        book = Book.objects.get(pk = book_pk)
        user = data.get("username")
        user = User.objects.get(username = user)
        review = data.get("review")

        new_thread = Thread.objects.create(
            user=user,
            book=book,
            review=review,
        )

        new_thread.save()

        return JsonResponse({"status": True}, status=200)
    else:
        return JsonResponse({"status": False}, status=401)