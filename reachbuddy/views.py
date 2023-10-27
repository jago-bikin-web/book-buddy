from django.shortcuts import render
from django.http import HttpResponseRedirect
from reachbuddy.models import Thread
from reachbuddy.forms import ThreadForm
from django.urls import reverse

# Create your views here.
def show_reachbuddy(request):
    threads = Thread.objects.all()

    context = {
        'name': 'User1',
        'threads': threads
    }

    return render(request, "reachbuddy.html", context)

def create_thread(request):
    form = ThreadForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('reachbuddy:show_reachbuddy'))

    context = {'form': form}
    return render(request, "create_thread.html", context)