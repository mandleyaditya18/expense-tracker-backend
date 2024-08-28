from django.db import models
from django.contrib.auth.models import AbstractUser
from common.constants import CURRENCY_CHOICES

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True)
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES, default="INR")
