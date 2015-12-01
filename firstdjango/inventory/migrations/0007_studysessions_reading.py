# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20151130_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='studysessions',
            name='reading',
            field=models.ForeignKey(default=1, to='inventory.Item'),
            preserve_default=False,
        ),
    ]
