# Generated by Django 2.2.6 on 2019-11-03 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2client.contrib.django_util.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialsModel',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credential', oauth2client.contrib.django_util.models.CredentialsField(null=True)),
                ('task', models.CharField(max_length=80, null=True)),
                ('updated_time', models.CharField(max_length=80, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onid', models.CharField(max_length=25, unique=True, verbose_name='ONID')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('phone_number', models.CharField(max_length=25, verbose_name='phone number')),
                ('creator_privilege', models.BooleanField(verbose_name='creator')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(max_length=50, verbose_name='start time')),
                ('end', models.DateTimeField(max_length=50, verbose_name='end time')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('num_people', models.IntegerField(verbose_name='max number of people')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.User')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Slot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.User')),
            ],
            options={
                'unique_together': {('user', 'slot')},
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('type', models.CharField(max_length=50, verbose_name='type')),
                ('path', models.CharField(max_length=500, verbose_name='path')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Reservation')),
            ],
            options={
                'unique_together': {('name', 'path')},
            },
        ),
    ]