# Generated by Django 3.2.15 on 2022-09-15 11:17

import pytz
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0072_alter_githubissue_type'),
    ]

    beginning_of_time = datetime.datetime(2020, 1, 1, 0, 0, tzinfo=pytz.UTC)

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=beginning_of_time),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='result',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=beginning_of_time),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]