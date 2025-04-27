from django.db import models
from django.contrib.auth.models import User
import os

class Education(models.Model):
    name = models.CharField("Уровень образования", max_length=100)

    def __str__(self):
        return self.name

class ZodiacSign(models.Model):
    name = models.CharField("Название знака", max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):  # Новая модель для городов
    name = models.CharField("Название города", max_length=100)

    def __str__(self):
        return self.name

class HobbyGroup(models.Model):
    name = models.CharField("Название группы", max_length=100)

    def get_hobby_ids(self):
        return ", ".join([str(h.id) for h in self.hobby_set.all()])

    def __str__(self):
        return self.name

class Hobby(models.Model):
    name = models.CharField("Название", max_length=100)
    group = models.ForeignKey(
        HobbyGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Группа"
    )

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
    zodiac_sign = models.ForeignKey(
        ZodiacSign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Знак зодиака"
    )
    education = models.ForeignKey(
        Education,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Образование"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to = 'user_photos/',
        default='user_photos/photo_base.jpg',
        null = True,
        blank = True
    )
    hobbies = models.ManyToManyField(Hobby, blank=True)
    children_count = models.IntegerField(null=True, blank=True)
    hobby_description = models.TextField(blank=True, null=True)
    life_goal = models.TextField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)
    SEX_CHOICES = [
        (1, 'Мужской'),
        (2, 'Женский'),
    ]
    sex = models.IntegerField(
        choices=SEX_CHOICES,
        null=True,
        blank=True,
        default=1,
        verbose_name="Пол"
    )
    city = models.PositiveSmallIntegerField(('city'), choices=CITIES, blank=True, default=1) #!временно пустые строки разрешены, сначала раздадим всем пользователям города

    weights_for_ahp = models.CharField(max_length = 100, null=True)
    user_CR = models.PositiveSmallIntegerField(default=0)

    city_vs_hobby = models.PositiveIntegerField(default=3)
    city_vs_zodiac = models.PositiveIntegerField(default=3)
    city_vs_education = models.PositiveIntegerField(default=3)
    education_vs_hobby = models.PositiveIntegerField(default=3)
    education_vs_zodiac = models.PositiveIntegerField(default=3)
    hobby_vs_zodiac = models.PositiveIntegerField(default=3)

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

class UserFilters(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.PositiveSmallIntegerField(blank=True, null=True)
    zodiac_sign = models.ForeignKey(ZodiacSign, null=True, blank=True, on_delete=models.SET_NULL)
    education = models.ForeignKey(Education, null=True, blank=True, on_delete=models.SET_NULL)
    hobbies = models.ManyToManyField(Hobby, blank=True)
