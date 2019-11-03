# Generated by Django 2.2.6 on 2019-10-28 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_auto_20191028_0156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slot',
            old_name='end_time',
            new_name='EndTime',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='location',
            new_name='Location',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='creator',
            new_name='Owner',
        ),
        migrations.RenameField(
            model_name='slot',
            old_name='start_time',
            new_name='StartTime',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='num_people',
        ),
    ]