# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-27 20:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('visualize', '0010_auto_20160827_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='figure',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='figure',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 27, 20, 23, 21, 563367, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
