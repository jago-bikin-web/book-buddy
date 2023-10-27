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
from findbuddy.models import FindBook

# Create your views here.

def show_findbuddy(request):
    books = FindBook.objects.all()

    categories = set([categories for book in books])
    
    context = {
        'name' : 'Gamma',
        'books' : books,
        'categories': categories,
    }


    return render(request, "findbuddy.html", context)

def get_book_json(request):
    book_item = FindBook.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))
