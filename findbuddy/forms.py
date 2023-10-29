from django.forms import ModelForm
from book.models import Book

class RatingsForm(ModelForm):
    class Meta:
        model = Book
        fields = ["average_rating"]