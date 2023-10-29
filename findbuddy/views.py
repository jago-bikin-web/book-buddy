from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from book.models import Book
from findbuddy.models import BookFind
from findbuddy.forms import BookForm

# Create your views here.
def show_json(request):
    data = BookFind.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def add_rating(request):
    print(request.POST)
    print(request.POST.get("pk"))
    print(request.POST.get("form"))
    return JsonResponse("Hallooo")

@login_required(login_url='main:login')
def show_findbuddy(request):
    books = Book.objects.all()
    form = BookForm(request.POST or None)
    categories = set([book.categories for book in books])

    context = {
        'books' : books,
        'categories': categories,
        'form': form
    }

    return render(request, "findbuddy.html", context)

def get_book_json(request):
    book_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))

@csrf_exempt
def add_request_ajax(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")

        new_request = BookFind(title=title, author=author)
        new_request.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


def get_request_json(request):
    request_item = BookFind.objects.all()
    return HttpResponse(serializers.serialize('json', request_item))
