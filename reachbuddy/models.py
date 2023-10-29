from django.db import models
from django.contrib.auth.models import User
from main.models import Profile
from book.models import Book

# Create your models here.

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)