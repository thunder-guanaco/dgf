# Generated by Django 3.2.13 on 2022-05-02 20:49

from django.db import migrations, models


def deactivate_bag_tag_changes_with_equal_previous_and_new_number(apps, schema_editor):
    BagTagChange = apps.get_model('dgf', 'BagTagChange')
    for bag_tag_change in BagTagChange.objects.all():
        if bag_tag_change.previous_number == bag_tag_change.new_number:
            bag_tag_change.active = False
            bag_tag_change.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0067_auto_20220430_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='bagtagchange',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(deactivate_bag_tag_changes_with_equal_previous_and_new_number),
    ]