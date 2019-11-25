# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-24 19:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_scheduleuser_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(max_length=50, verbose_name='start time')),
                ('end', models.DateTimeField(max_length=50, verbose_name='end time')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('num_people', models.IntegerField(verbose_name='max number of people')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
