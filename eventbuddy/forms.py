from django.forms import ModelForm
from eventbuddy.models import Event
from django import forms

class EventForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Event
        fields = ["name", "date", "description"]