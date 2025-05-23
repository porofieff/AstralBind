# Generated by Django 5.1.7 on 2025-05-01 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0020_userprofile_city_vs_education_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('favorite_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='lk.userprofile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='lk.userprofile')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('user', 'favorite_user')},
            },
        ),
    ]
