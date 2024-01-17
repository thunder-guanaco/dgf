import partial_date.fields
from django.db import migrations
from partial_date import PartialDate


def convert_dates(apps, schema_editor):
    Ace = apps.get_model('dgf', 'Ace')
    for ace in Ace.objects.all():
        ace.partial_date = PartialDate(ace.date, precision=PartialDate.DAY) if ace.date else None
        ace.save()


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0017_friend_club_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='ace',
            name='partial_date',
            field=partial_date.fields.PartialDateField(blank=True, null=True),
        ),
        migrations.RunPython(convert_dates),
        migrations.RemoveField(
            model_name='ace',
            name='date',
        ),
        migrations.RenameField(
            model_name='ace',
            old_name='partial_date',
            new_name='date',
        ),
    ]
