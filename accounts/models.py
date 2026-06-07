from django.db import models
from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    avater = models.ImageField(upload_to='avaters/', null=True, blank=True)

    def __str__(self):
        return self.username