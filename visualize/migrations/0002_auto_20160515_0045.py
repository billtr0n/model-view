# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualize', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='comments',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='groups',
            field=models.ManyToManyField(blank=True, to='visualize.Group'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='projects',
            field=models.ManyToManyField(blank=True, to='visualize.Project'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='tags',
            field=models.ManyToManyField(blank=True, to='visualize.Tag'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='upload_date',
            field=models.DateTimeField(blank=True, verbose_name='upload date'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='user',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]