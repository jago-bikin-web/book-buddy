from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from main.forms import SignUpForm
from main.models import Profile

def show_landing_page(request):
    return render(request, "main.html")

def signup(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(
                user = new_user,
                status = new_user.status,
                full_name = new_user.full_name,
                email = new_user.email
                )
            messages.success(request, 'Sign up successful!')
            return redirect('main:login_user')
    
    context = {'form':form}
    return render(request, 'signup.html', context)
