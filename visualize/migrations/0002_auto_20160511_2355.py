# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-12 06:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visualize', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='name',
            field=models.CharField(default='unknown', max_length=200),
        ),
        migrations.AlterField(
            model_name='data_product',
            name='simulation',
            field=models.ForeignKey(default='unknown', on_delete=django.db.models.deletion.CASCADE, to='visualize.Simulation'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='upload_date',
            field=models.DateTimeField(verbose_name='upload date'),
        ),
    ]
