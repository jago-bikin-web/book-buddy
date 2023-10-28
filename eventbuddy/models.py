from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class Event(models.Model):
    #buku = models.OneToOneField(Book, on_delete=models.CASCADE, unique=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()

    def count(self):
        return Registration.objects.filter(event=self).count()
    
class Registration(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


# Create your models here.
