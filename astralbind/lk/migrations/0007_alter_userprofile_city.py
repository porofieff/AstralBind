from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0006_userprofile_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Москва'), (2, 'Санкт-Петербург'), (3, 'Новосибирск'), (4, 'Екатеринбург'), (5, 'Казань'), (6, 'Нижний Новгород'), (7, 'Челябинск'), (8, 'Самара'), (9, 'Омск'), (10, 'Ростов-на-Дону'), (11, 'Уфа'), (12, 'Красноярск'), (13, 'Воронеж'), (14, 'Пермь'), (15, 'Волгоград'), (16, 'Краснодар'), (17, 'Саратов'), (18, 'Тюмень'), (19, 'Тольятти'), (20, 'Ижевск'), (21, 'Липецк'), (22, 'Северодвинск')], default=1, verbose_name='city'),
        ),
    ]
