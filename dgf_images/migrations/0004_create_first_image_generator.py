from django.db import migrations


def create_image_generators(apps, schema_editor):
    ImageGenerator = apps.get_model('dgf_images', 'ImageGenerator')
    ImageGenerator.objects.create(name='All Friends Background With Text', slug='all-friends-background-with-text')


class Migration(migrations.Migration):
    dependencies = [
        ('dgf_images', '0003_auto_20221121_2328'),
    ]

    operations = [
        migrations.RunPython(create_image_generators),
    ]
