# Generated by Django 3.2.23 on 2024-01-16 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dgf_league', '0010_rename_date_match_created'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='team',
            name='unique_team_name',
        ),
    ]
