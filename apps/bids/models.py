from django.db import models
from apps.base.models import AppUser


class Bid(AppUser):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
