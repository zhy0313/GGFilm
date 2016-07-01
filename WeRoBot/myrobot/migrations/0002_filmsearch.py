# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Film', models.CharField(max_length=100, verbose_name=b'Film', db_index=True)),
                ('Developer', models.CharField(max_length=100, verbose_name=b'Developer', db_index=True)),
                ('Dilution', models.CharField(max_length=100, verbose_name=b'Dilution', db_index=True)),
                ('ASA_ISO', models.CharField(max_length=100, verbose_name=b'ASA/ISO', db_index=True)),
                ('a35mm', models.CharField(max_length=100, verbose_name=b'a35mm')),
                ('a120', models.CharField(max_length=100, verbose_name=b'a120')),
                ('Sheet', models.CharField(max_length=100, verbose_name=b'Sheet')),
                ('Temp', models.CharField(max_length=100, verbose_name=b'Temp')),
                ('Notes', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Massive Dev Chart',
                'verbose_name_plural': 'Massive Dev Chart',
            },
        ),
    ]
