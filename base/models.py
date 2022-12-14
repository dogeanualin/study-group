

from email.policy import default
from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
from numpy import require
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default = 'avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topyc(models.Model):
    name = models.CharField(max_length=200)


    def __str__(self) -> str:
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    topic = models.ForeignKey(Topyc,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    #participants=
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-updated','-created']


class Messages(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated','-created']


    def __str__(self) -> str:
        return self.body[0:50]

