# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20151015_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudySessions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('startPage', models.IntegerField()),
                ('pagesRead', models.IntegerField()),
                ('timeSpent', models.IntegerField()),
            ],
        ),
    ]
