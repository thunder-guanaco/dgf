# Generated by Django 2.2.17 on 2021-03-08 11:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0027_auto_20201206_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='udisc_username',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='UDisc Username'),
        ),
    ]
