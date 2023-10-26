from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #NANTI PAS RESTU UDAH KELAR REGIS DAN VIEWS USERNYA

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()