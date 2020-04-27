# Generated by Django 3.0.2 on 2020-04-27 10:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorrequest',
            name='student_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='tutor_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tutorrequest',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 27, 10, 55, 47, 151229, tzinfo=utc)),
        ),
    ]