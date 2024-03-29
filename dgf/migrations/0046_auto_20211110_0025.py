# Generated by Django 2.2.17 on 2021-11-09 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0045_auto_20211109_2246'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.UniqueConstraint(fields=('pdga_id',), name='unique_pdga_id_for_tournament'),
        ),
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.UniqueConstraint(fields=('gt_id',), name='unique_gt_id_for_tournament'),
        ),
        migrations.AddConstraint(
            model_name='tournament',
            constraint=models.UniqueConstraint(fields=('metrix_id',), name='unique_metrix_id_for_tournament'),
        ),
    ]
