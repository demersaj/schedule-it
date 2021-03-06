# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-24 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20191124_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('path', models.CharField(max_length=500, verbose_name='path')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Reservation')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set([('name', 'path')]),
        ),
    ]
