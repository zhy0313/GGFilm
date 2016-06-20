# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0004_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ItemPicId', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemTitle', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemShopName', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemLocation', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemPrice', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemTaoBaoPrice', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemDeal', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Item Storage',
                'verbose_name_plural': 'Item Storage',
            },
        ),
        migrations.CreateModel(
            name='TempItemStorage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ItemPicId', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemTitle', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemShopName', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemLocation', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemPrice', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemTaoBaoPrice', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('ItemDeal', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Temporary Item Storage',
                'verbose_name_plural': 'Temporary Item Storage',
            },
        ),
    ]
