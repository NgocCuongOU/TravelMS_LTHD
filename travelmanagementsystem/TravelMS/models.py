from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    image = models.ImageField(upload_to='posts/%Y/%m', default=None)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name