from django.shortcuts import render


def show_my_buddy(request):
    return render(request, "main.html")

