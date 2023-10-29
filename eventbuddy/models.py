from django.db import models
from django.contrib.auth.models import User
from book.models import Book
from main.models import Profile


class Event(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20)
    date = models.DateField()
    description = models.TextField(max_length=50)
    participant = models.ManyToManyField(Profile, null=True)
    
