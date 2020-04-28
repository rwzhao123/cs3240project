# Generated by Django 3.0.2 on 2020-04-28 02:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200427_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorrequest',
            name='student_message',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='tutor_message',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tutorrequest',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 28, 2, 1, 21, 712649, tzinfo=utc)),
        ),
    ]