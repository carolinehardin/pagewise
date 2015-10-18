# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='amount',
            new_name='endPage',
        ),
        migrations.RemoveField(
            model_name='item',
            name='description',
        ),
        migrations.AddField(
            model_name='item',
            name='course',
            field=models.CharField(default='Biology', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='dueDate',
            field=models.DateField(default=datetime.datetime(2015, 10, 15, 2, 15, 48, 453650, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='startPage',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
