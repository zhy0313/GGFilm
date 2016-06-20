# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0002_filmsearch'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notes',
        ),
    ]
