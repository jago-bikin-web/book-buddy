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
from findbuddy.forms import RatingsForm

# Create your views here.
@csrf_exempt
def add_rating(request):
    form = RatingsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()

    print(request.POST)
    print(request.POST.get("pk"))
    print(request.POST.get("form"))


def show_findbuddy(request):
    books = Book.objects.all()

    form = RatingsForm(request.POST or None)

    categories = set([book.categories for book in books])
    
    context = {
        'name' : 'Gamma',
        'books' : books,
        'categories': categories,
        'form' : form,
    }

    return render(request, "findbuddy.html", context)

def get_book_json(request):
    book_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))

# def get_book_
