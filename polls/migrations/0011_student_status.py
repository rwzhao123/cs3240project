# Generated by Django 3.0.2 on 2020-04-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20200414_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
