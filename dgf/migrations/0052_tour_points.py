# Generated by Django 2.2.17 on 2021-11-15 21:30

from django.db import migrations

from dgf.tour import TS_POINTS_PLUS_BEATEN_PLAYERS


def re_calculate_ts_points(apps, schema_editor):
    Tournament = apps.get_model('dgf', 'Tournament')
    for tournament in Tournament.objects.filter(name__startswith='Tremonia Series #'):
        tournament.point_system = TS_POINTS_PLUS_BEATEN_PLAYERS
        tournament.save()
        for result in tournament.results.all():
            result.save()


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0051_auto_20211115_2230'),
    ]

    operations = [
        migrations.RunPython(re_calculate_ts_points),
    ]
