# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0008_tempitemstorage_has_been_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemstorage',
            name='ItemProductName',
            field=models.CharField(default=datetime.datetime(2016, 10, 13, 5, 27, 20, 759300, tzinfo=utc), max_length=200, verbose_name='\u5546\u54c1\u540d\u79f0'),
            preserve_default=False,
        ),
    ]
