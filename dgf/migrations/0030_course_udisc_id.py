# Generated by Django 2.2.17 on 2021-03-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0029_coursepluginmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='udisc_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='UDisc ID'),
        ),
    ]