# Generated by Django 2.2.11 on 2020-03-29 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
