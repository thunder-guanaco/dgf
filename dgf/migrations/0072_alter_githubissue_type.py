# Generated by Django 3.2.15 on 2022-08-15 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0071_auto_20220816_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubissue',
            name='type',
            field=models.CharField(choices=[('F', 'Feedback'), ('L', 'Live Error'), ('M', 'Management Command Error')],
                                   default='F',
                                   max_length=1,
                                   verbose_name='Type'),
        ),
    ]