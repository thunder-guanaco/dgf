# Generated by Django 3.2.12 on 2022-03-17 21:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0062_rename_bagtagchange2_bagtagchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bagtagchange',
            name='new_number',
            field=models.PositiveIntegerField(default=None, validators=[django.core.validators.MinValueValidator(1)],
                                              verbose_name='New number'),
            preserve_default=False,
        ),
    ]
