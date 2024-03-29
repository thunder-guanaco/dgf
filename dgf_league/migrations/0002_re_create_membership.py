# Generated by Django 3.2.16 on 2023-01-14 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0078_allow_2_different_results_for_the_same_tournament'),
        ('dgf_league', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TeamMembership',
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships',
                                             to='dgf.friend', verbose_name='Friend')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members',
                                           to='dgf_league.team', verbose_name='Team')),
            ],
        ),
        migrations.AddConstraint(
            model_name='teammembership',
            constraint=models.UniqueConstraint(fields=('friend',), name='only_one_team_per_friend'),
        ),
    ]
