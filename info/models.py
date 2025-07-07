from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)
    role = models.CharField(default='user', max_length=10)

    def __str__(self):
        return self.user.username
