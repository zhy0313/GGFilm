# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0007_auto_20160619_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempitemstorage',
            name='Has_Been_Selected',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u52a0\u5165\u4ef7\u683c\u8ddf\u8e2a\u961f\u5217'),
        ),
    ]
