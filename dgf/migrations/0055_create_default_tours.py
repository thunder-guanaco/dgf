from django.db import migrations


def create_default_tour(apps, schema_editor):
    Tour = apps.get_model('dgf', 'Tour')
    Tournament = apps.get_model('dgf', 'Tournament')

    tour, _ = Tour.objects.get_or_create(name='Ewige Tabelle')
    tour.evaluate_how_many = 10000
    tour.save()

    for tournament in Tournament.objects.filter(name__startswith='Tremonia Series #'):
        tour.tournaments.add(tournament)


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0054_tour_evaluate_how_many'),
    ]

    operations = [
        migrations.RunPython(create_default_tour),
    ]
