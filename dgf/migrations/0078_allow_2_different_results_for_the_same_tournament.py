# Generated by Django 3.2.16 on 2022-11-30 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0077_githubissue_timestamp'),
    ]

    # Django allows you to define custom UniqueConstraints to define which combinations of value in a row are allowed,
    # but removing these later can be problematic when some ForeignKey is involved, at least with MySQL it may throw a
    # `Cannot drop index '...': needed in a foreign key constraint`
    # at you.
    # That's why this migration was generated in 3 steps following this:
    # https://gist.github.com/cb109/847df8376234fa02814debec9f3d26bc
    operations = [

        # Step 1: Tell Django that we don't want an index and constraint on the ForeignKey
        migrations.AlterField(
            model_name='result',
            name='friend',
            field=models.ForeignKey(db_constraint=False, db_index=False, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='results', to='dgf.friend', verbose_name='Player'),
        ),
        migrations.AlterField(
            model_name='result',
            name='tournament',
            field=models.ForeignKey(db_constraint=False, db_index=False, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='results', to='dgf.tournament', verbose_name='Tournament'),
        ),

        # Step 2: Remove the custom UniqueConstrain
        migrations.RemoveConstraint(
            model_name='result',
            name='the same tournament can not be played twice by the same friend',
        ),

        # Step 3: Re-introduce the default behaviour of having an index and constraint on the ForeignKey
        migrations.AddField(
            model_name='result',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results',
                                    to='dgf.friend', verbose_name='Player'),
        ),
        migrations.AlterField(
            model_name='result',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results',
                                    to='dgf.tournament', verbose_name='Tournament'),
        ),
        migrations.AddConstraint(
            model_name='result',
            constraint=models.UniqueConstraint(fields=('tournament', 'friend', 'active'),
                                               name='friend_can_not_play_same_tournament_twice'),
        ),
    ]
