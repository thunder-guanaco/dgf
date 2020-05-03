# Generated by Django 2.2.11 on 2020-05-03 12:06

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import django_countries.fields
import partial_date.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0019_auto_20200501_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ace',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dgf.Course',
                                    verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='ace',
            name='date',
            field=partial_date.fields.PartialDateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='ace',
            name='disc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dgf.Disc',
                                    verbose_name='Disc'),
        ),
        migrations.AlterField(
            model_name='ace',
            name='hole',
            field=models.CharField(max_length=20, verbose_name='Hole'),
        ),
        migrations.AlterField(
            model_name='ace',
            name='type',
            field=models.CharField(choices=[('P', 'Practice'), ('C', 'Casual Round'), ('T', 'Tournament')],
                                   max_length=1, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='course',
            name='city',
            field=models.CharField(max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='course',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='postal_code',
            field=models.CharField(max_length=10, verbose_name='Postal code'),
        ),
        migrations.AlterField(
            model_name='disc',
            name='display_name',
            field=models.CharField(max_length=200, verbose_name='Display name'),
        ),
        migrations.AlterField(
            model_name='disc',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Manufacturer'),
        ),
        migrations.AlterField(
            model_name='disc',
            name='mold',
            field=models.CharField(max_length=200, unique=True, verbose_name='Mold'),
        ),
        migrations.AlterField(
            model_name='discinbag',
            name='amount',
            field=models.PositiveIntegerField(default=1, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='discinbag',
            name='disc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dgf.Disc', verbose_name='Scheibe'),
        ),
        migrations.AlterField(
            model_name='discinbag',
            name='type',
            field=models.CharField(
                choices=[('P', 'Putter'), ('M', 'Mid-range'), ('F', 'Fairway driver'), ('D', 'Distance driver')],
                max_length=1, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='division',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='division',
            name='text',
            field=models.CharField(max_length=100, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='feedback',
            field=models.TextField(verbose_name='Feedback'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='friend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dgf.Friend',
                                    verbose_name='Friend'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='club_role',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Club role'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='dgf.Division', verbose_name='Division'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='favorite_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='dgf.Course', verbose_name='Favorite course'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='free_text',
            field=models.TextField(blank=True, null=True, verbose_name='Started playing'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='main_photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Main photo'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nickname'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='pdga_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='PDGA Number'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='plays_since',
            field=models.PositiveIntegerField(blank=True, null=True,
                                              validators=[django.core.validators.MinValueValidator(1926)],
                                              verbose_name='Plays since'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True,
                                              validators=[django.core.validators.MaxValueValidator(2000)],
                                              verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='sponsor',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Sponsor'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='sponsor_link',
            field=models.URLField(blank=True, null=True, verbose_name='Sponsor link'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='sponsor_logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Sponsor logo'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='total_earnings',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10,
                                      verbose_name='Total earnings'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='total_tournaments',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total tournaments'),
        ),
        migrations.AlterField(
            model_name='highlight',
            name='content',
            field=models.CharField(max_length=100, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='video',
            name='type',
            field=models.CharField(choices=[('B', 'In the bag'), ('A', 'Ace'), ('O', 'Other')], default='O',
                                   max_length=1, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
    ]
