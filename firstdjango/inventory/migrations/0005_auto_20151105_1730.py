# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course',
            new_name='title',
        ),
    ]
