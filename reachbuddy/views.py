from django.shortcuts import render

# Create your views here.
def show_reachbuddy(request):
    context = {
        'name': 'User1'
    }

    return render(request, "reachbuddy.html", context)