# Generated by Django 2.2.6 on 2019-10-28 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20191028_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='Subject',
            field=models.CharField(default='Work on project', max_length=100, verbose_name='subject'),
            preserve_default=False,
        ),
    ]
