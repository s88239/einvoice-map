# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('shop', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
