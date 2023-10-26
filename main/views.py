from random import randint

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers

from main.models import Profile


def show_landing_page(request):
    return render(request, "main.html")

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
            
            new_user = Profile(user=user, full_name=full_name, email=email, status=status, profile_picture=f"https://i.pravatar.cc/48?={randint(0,100)}")

            new_user.save()
            return redirect('main:login')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
            return redirect('main:register')

    return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:landing_page"))
            response.set_cookie('user', user)
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
            return redirect('main:login')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    return response