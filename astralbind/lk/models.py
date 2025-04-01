from django.db import models
from django.contrib.auth.models import User

class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    children_count = models.IntegerField(null=True, blank=True)
    hobby_description = models.TextField(blank=True, null=True)
    life_goal = models.TextField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
