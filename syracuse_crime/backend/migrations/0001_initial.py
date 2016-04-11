# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crime_type', models.CharField(max_length=56)),
                ('address', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=128)),
                ('date_time', models.DateTimeField()),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
            ],
        ),
    ]
