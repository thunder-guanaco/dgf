# Generated by Django 3.2.23 on 2024-01-17 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dgf_league', '0013_fill_teammembership_result'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.DeleteModel(
            name='TeamMembership',
        ),
    ]
