# Generated by Django 2.2.11 on 2020-04-19 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0009_auto_20200419_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='sponsor',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='friend',
            name='sponsor_logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
