# Generated by Django 2.2.13 on 2020-06-29 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0025_auto_20200627_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance',
                                             to='dgf.Friend', verbose_name='Player')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance',
                                                 to='dgf.Tournament', verbose_name='Tournament')),
            ],
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(fields=('tournament', 'friend'),
                                               name='the same tournament can not be attended twice'),
        ),
    ]