# Generated by Django 3.2.23 on 2024-01-15 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dgf_league', '0009_alter_friendwithoutteam_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='date',
            new_name='created',
        ),
    ]