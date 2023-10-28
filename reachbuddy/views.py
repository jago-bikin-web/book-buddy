from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from reachbuddy.models import Thread
from reachbuddy.forms import ThreadForm
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

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

def show_json(request):
    data = Thread.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def trash_thread(request, id):
    thread = Thread.objects.get(id=id)
    thread.delete()

    response = HttpResponseRedirect(reverse("reachbuddy:show_reachbuddy"))
    return response