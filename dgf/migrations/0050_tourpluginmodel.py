# Generated by Django 2.2.17 on 2021-11-15 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('dgf', '0049_auto_20211115_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourPluginModel',
            fields=[
                ('cmsplugin_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, related_name='dgf_tourpluginmodel', serialize=False,
                                      to='cms.CMSPlugin')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dgf.Tour')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
