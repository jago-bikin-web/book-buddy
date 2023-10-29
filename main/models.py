from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    status = models.CharField(max_length=1)
    profile_picture = models.URLField()

    def is_reguler(self):
        if self.status == 'R':
            return True
        return False

    def is_member(self):
        if self.status == 'M':
            return True
        return False

    def __str__(self):
        return self.user.username
