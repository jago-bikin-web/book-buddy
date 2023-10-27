from django.forms import ModelForm
from reachbuddy.models import Thread

class ThreadForm(ModelForm):
    class Meta:
        model = Thread
        fields = ["review"]