import re

from django.db import migrations, models


def fill_display_name(apps, schema_editor):
    Disc = apps.get_model('dgf', 'Disc')
    for disc in Disc.objects.all():
        disc.display_name = re.sub(r' *\(.*\)', '', disc.mold)
        disc.save()


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0014_friend_sponsor_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='disc',
            name='display_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='disc',
            name='mold',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.RunPython(fill_display_name),
        migrations.AlterField(
            model_name='disc',
            name='display_name',
            field=models.CharField(max_length=200),
        ),
    ]
