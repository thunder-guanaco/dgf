# Generated by Django 3.2.12 on 2022-03-17 21:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0061_auto_20220317_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='BagTagChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_number', models.PositiveIntegerField(blank=True, null=True,
                                                           validators=[django.core.validators.MinValueValidator(1)],
                                                           verbose_name='New number')),
                ('previous_number', models.PositiveIntegerField(blank=True, null=True, validators=[
                    django.core.validators.MinValueValidator(1)], verbose_name='Previous number')),
                ('timestamp', models.DateTimeField()),
                ('actor',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_bag_tag_changes',
                                   to='dgf.friend', verbose_name='Actor')),
                ('friend',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bag_tag_changes',
                                   to='dgf.friend', verbose_name='Player')),
            ],
        ),
        migrations.DeleteModel(
            name='BagtagChange2',
        ),
    ]
