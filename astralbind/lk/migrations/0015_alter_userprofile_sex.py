# Generated by Django 5.1.7 on 2025-04-19 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lk', '0014_userprofile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
