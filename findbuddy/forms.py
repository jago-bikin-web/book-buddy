from django import forms
from findbuddy.models import BookFind

class BookForm(forms.ModelForm):
    class Meta:
        model = BookFind
        fields = ['title', 'author']