# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20151105_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studysessions',
            old_name='pagesRead',
            new_name='endPage',
        ),
    ]
