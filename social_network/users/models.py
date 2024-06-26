from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import UserManager

class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['id']  # Specify the default ordering

    def __str__(self):
        return self.username