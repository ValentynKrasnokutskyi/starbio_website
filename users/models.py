from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
        Custom user model extending Django's AbstractUser.
    """
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, verbose_name="Photo")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Date of Birth")
