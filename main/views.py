from random import randint

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from main.models import Profile
from mybuddy.models import OwnedBook


def show_landing_page(request):
    
    context = {
        'user': None,
        'profile_picture': None
    }
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        profile_picture = user.profile_picture
        context = {
            'user': user.full_name,
            'profile_picture': profile_picture
        }

    return render(request, "main.html", context)

@login_required(login_url='main:login')
def home(request):
    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture
    banyak_buku = len(OwnedBook.objects.filter(user=user))

    context = {
        'user': user.full_name,
        'profile_picture': profile_picture,
        'buku' : banyak_buku
    }

    return render(request, "home.html", context)

def register_user(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        status = request.POST.get("status")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1)
            
            new_user = Profile(user=user, full_name=full_name, email=email, status=status, profile_picture=f"https://i.pravatar.cc/48?img={randint(1,70)}")

            new_user.save()
            return redirect('main:login')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
            return redirect('main:register')
    
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        return render(request, 'signup.html')

def login_user(request):
    next = request.GET.get('next', None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_login = Profile.objects.get(user=user)
            if next:
                response = HttpResponseRedirect(next)
            else:
                response = HttpResponseRedirect(reverse(f"main:home"))
            response.set_cookie('user', user_login.full_name)
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
            return redirect('main:login')
        
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:landing_page'))
    response.delete_cookie('user')
    response.delete_cookie('profile_picture')
    return response
