# Generated by Django 3.0.2 on 2020-03-23 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='user',
            new_name='user_id',
        ),
    ]