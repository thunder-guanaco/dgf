# Generated by Django 2.2.17 on 2021-03-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0032_course_udisc_main_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='gt_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='GT Number'),
        ),
    ]
