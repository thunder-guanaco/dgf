# Generated by Django 2.2.17 on 2021-11-04 13:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0041_remove_friend_tremonia_series_wins'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Result',
        ),

        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)],
                                                         verbose_name='Position')),
                ('friend',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='dgf.Friend',
                                   verbose_name='Player')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results',
                                                 to='dgf.Tournament', verbose_name='Tournament')),
            ],
        ),
        migrations.AddConstraint(
            model_name='result',
            constraint=models.UniqueConstraint(fields=('tournament', 'friend'),
                                               name='the same tournament can not be played twice by the same friend'),
        ),
    ]
