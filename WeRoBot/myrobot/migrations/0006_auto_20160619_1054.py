# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0005_itemstorage_tempitemstorage'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemstorage',
            name='ItemLink',
            field=models.URLField(default=datetime.datetime(2016, 6, 19, 10, 54, 22, 280702, tzinfo=utc), verbose_name='\u5546\u54c1URL\u5730\u5740'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tempitemstorage',
            name='ItemLink',
            field=models.URLField(default=datetime.datetime(2016, 6, 19, 10, 54, 30, 563040, tzinfo=utc), verbose_name='\u5546\u54c1URL\u5730\u5740'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemDeal',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u4ea4\u6613\u91cf'),
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemLocation',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u6765\u6e90\u5730'),
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemPicId',
            field=models.CharField(max_length=200, verbose_name='\u5546\u54c1\u5c55\u793a\u56feID'),
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemPrice',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemShopName',
            field=models.CharField(max_length=200, verbose_name='\u5e97\u94fa\u540d'),
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemTaoBaoPrice',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u6dd8\u5b9d\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='itemstorage',
            name='ItemTitle',
            field=models.CharField(max_length=500, verbose_name='\u5546\u54c1\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemDeal',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u4ea4\u6613\u91cf'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemLocation',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u6765\u6e90\u5730'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemPicId',
            field=models.CharField(max_length=200, verbose_name='\u5546\u54c1\u5c55\u793a\u56feID'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemPrice',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemShopName',
            field=models.CharField(max_length=200, verbose_name='\u5e97\u94fa\u540d'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemTaoBaoPrice',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u6dd8\u5b9d\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='tempitemstorage',
            name='ItemTitle',
            field=models.CharField(max_length=500, verbose_name='\u5546\u54c1\u63cf\u8ff0'),
        ),
    ]
