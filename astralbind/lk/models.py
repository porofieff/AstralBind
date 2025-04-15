from django.db import models
from django.contrib.auth.models import User
import os

class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    CITIES = [
        (1, 'Москва'),
        (2, 'Санкт-Петербург'),
        (3, 'Новосибирск'),
        (4, 'Екатеринбург'),
        (5, 'Казань'),
        (6, 'Нижний Новгород'),
        (7, 'Челябинск'),
        (8, 'Самара'),
        (9, 'Омск'),
        (10, 'Ростов-на-Дону'),
        (11, 'Уфа'),
        (12, 'Красноярск'),
        (13, 'Воронеж'),
        (14, 'Пермь'),
        (15, 'Волгоград'),
        (16, 'Краснодар'),
        (17, 'Саратов'),
        (18, 'Тюмень'),
        (19, 'Тольятти'),
        (20, 'Ижевск'),
        (21, 'Липецк'),
        (22, 'Северодвинск'),
    ]
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
    city = models.PositiveSmallIntegerField(('city'), choices=CITIES, blank=True, default=1) #!временно пустые строки разрешены, сначала раздадим всем пользователям города

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
