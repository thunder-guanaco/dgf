# Generated by Django 2.2.11 on 2020-04-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0012_ace'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('feedback', models.TextField()),
            ],
        ),
    ]
