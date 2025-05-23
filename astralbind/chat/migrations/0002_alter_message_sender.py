# Generated by Django 5.1.7 on 2025-04-27 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        ('lk', '0020_userprofile_city_vs_education_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='lk.userprofile'),
        ),
    ]
