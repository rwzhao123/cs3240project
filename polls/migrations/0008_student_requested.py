# Generated by Django 3.0.2 on 2020-04-08 20:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0007_auto_20200408_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='requested',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
