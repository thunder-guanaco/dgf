# Generated by Django 3.2.20 on 2023-12-11 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('dgf', '0080_halloffamepluginmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementCommandExecution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.CharField(
                    choices=[('fetch_gt_data', 'fetch_gt_data'), ('fetch_pdga_data', 'fetch_pdga_data'),
                             ('fetch_tpl_data', 'fetch_tpl_data'), ('fetch_ts_data', 'fetch_ts_data'),
                             ('update_approved_discs', 'update_approved_discs'),
                             ('update_udisc_scores', 'update_udisc_scores')], max_length=50, verbose_name='Command')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('duration', models.PositiveIntegerField(verbose_name='Duration (in seconds)')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='executed_management_commands', to='dgf.friend',
                                            verbose_name='Actor')),
            ],
        ),
    ]