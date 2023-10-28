from django.db import models
from main.models import Profile
from book.models import Book


class OwnedBook(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    owned_book = models.OneToOneField(Book, on_delete=models.CASCADE)

    page_track = models.IntegerField()
    ulasan = models.TextField()

    # R = lagi dibaca, F = finish, W = wistlish
    status = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.user.full_name} - {self.owned_book.title}"