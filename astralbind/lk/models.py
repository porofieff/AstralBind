from django.db import models
from django.contrib.auth.models import User
import os

class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to = 'user_photos/',
        null = True,
        blank = True
    )
    hobbies = models.ManyToManyField(Hobby, blank=True)
    children_count = models.IntegerField(null=True, blank=True)
    hobby_description = models.TextField(blank=True, null=True)
    life_goal = models.TextField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Только для существующих объектов
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                if old_instance.photo and old_instance.photo != self.photo:
                    if os.path.isfile(old_instance.photo.path):
                        os.remove(old_instance.photo.path)
            except UserProfile.DoesNotExist:
                pass

        # Сохраняем новое фото
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.user.username}'
