# Generated by Django 2.2.17 on 2021-11-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0043_auto_20211105_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discinbag',
            name='type',
            field=models.CharField(
                choices=[('P', 'Putter'), ('M', 'Mid-Range'), ('F', 'Fairway Driver'), ('D', 'Distance Driver')],
                max_length=1, verbose_name='Type'),
        ),
    ]