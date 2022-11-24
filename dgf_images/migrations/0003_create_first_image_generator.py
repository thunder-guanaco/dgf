from django.db import migrations


def create_image_generators(apps, schema_editor):
    ImageGenerator = apps.get_model('dgf_images', 'ImageGenerator')
    ImageGenerator.objects.create(name='All Friends Background With Text', slug='all-friends-background-with-text')


class Migration(migrations.Migration):
    dependencies = [
        ('dgf_images', '0002_imagegenerator_active'),
    ]

    operations = [
        migrations.RunPython(create_image_generators),
    ]
