from django.shortcuts import render
from django.http import *
from django.urls import reverse
from book.models import Book
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

# Create your views here.

def show_findbuddy(request):
    books = Book.objects.all()

    # if 'last_login' in request.COOKIES:
    #     last_login = request.COOKIES['last_login']
    # else:
    #     last_login = 'N/A'
    
    context = {
        'name' : 'Gamma',
        'books' : books,
    }

    return render(request, "findbuddy.html", context)

def get_book_json(request):
    book_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))
