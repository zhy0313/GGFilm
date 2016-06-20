# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0003_delete_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Notes', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('Remark', models.CharField(max_length=200, verbose_name=b'Remark')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': "Notes' Remark",
                'verbose_name_plural': "Notes' Remark",
            },
        ),
    ]
