from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.

class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='thread_like')

    review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def number_of_likes(self):
        return self.likes.count()