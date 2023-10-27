from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Profile

@login_required(login_url='main:login')
def show_my_buddy(request):
    user = request.COOKIES.get('user', None)

    user = Profile.objects.get(full_name=user)
    profile_picture = user.profile_picture

    context = {
        'user': user.full_name,
        'profile_picture': profile_picture
    }
    return render(request, "mybuddy.html", context)

