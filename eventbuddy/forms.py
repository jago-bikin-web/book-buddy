from django.forms import ModelForm
from eventbuddy.models import Event
from django import forms
from book.models import Book

class EventForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="Choose Book")

    class Meta:
        model = Event
        fields = ["name", "date", "description","book"]