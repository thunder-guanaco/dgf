# Generated by Django 3.2.15 on 2022-08-15 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dgf', '0070_auto_20220621_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('body', models.TextField(blank=True, null=True, verbose_name='Body')),
                ('type', models.CharField(choices=[('F', 'Feedback'),
                                                   ('L', 'Live Error'),
                                                   ('M', 'Management Command Error')],
                                          max_length=1,
                                          verbose_name='Type')),
                ('friend', models.ForeignKey(null=True,
                                             on_delete=django.db.models.deletion.CASCADE,
                                             to='dgf.friend',
                                             verbose_name='Friend')),
            ],
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
