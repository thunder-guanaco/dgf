# Generated by Django 3.2.16 on 2023-01-25 12:50

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0078_allow_2_different_results_for_the_same_tournament'),
        ('dgf_league', '0005_alter_match_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.DeleteModel(
            name='Match',
        ),
        migrations.DeleteModel(
            name='TeamMembership',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_matches',
                                            to='dgf.friend', verbose_name='Actor')),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0),
                                                                   django.core.validators.MaxValueValidator(10)],
                                                       verbose_name='Points')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results',
                                            to='dgf_league.match', verbose_name='Match')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_teams',
                                            to='dgf.friend', verbose_name='Actor')),
            ],
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
        migrations.AddField(
            model_name='result',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results',
                                    to='dgf_league.team', verbose_name='Team'),
        ),
        migrations.AddConstraint(
            model_name='teammembership',
            constraint=models.UniqueConstraint(fields=('friend',), name='only_one_team_per_friend'),
        ),
        migrations.AddConstraint(
            model_name='team',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_team_name'),
        ),
        migrations.AddConstraint(
            model_name='result',
            constraint=models.UniqueConstraint(fields=('match', 'team'), name='teams_can_not_play_against_themselves'),
        ),
    ]
