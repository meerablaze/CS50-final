from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

import os
# Create your models here.

class User(AbstractUser):
    pass

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class New(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='new_creator')
    title = models.TextField(max_length=160)
    content = models.TextField(default='')
    description= models.TextField(default='')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="new_category", blank=True, null=True)
    new_date = models.DateField(default=datetime.now(), blank=True)
    new_date_upload = models.DateTimeField(default=datetime.now())
    city = models.TextField(max_length=80, default="Crespo")
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField(default=datetime.now(), blank=True)
