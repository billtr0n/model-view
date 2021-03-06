# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-28 18:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Figure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('title', models.TextField(blank=True, null=True)),
                ('file_path', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'get_latest_by': 'modified_date',
            },
        ),
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True, unique=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Simulation_Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(blank=True, max_length=200, null=True)),
                ('field', models.CharField(max_length=200)),
                ('val', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Simulation_Output',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=200)),
                ('field', models.CharField(max_length=200)),
                ('shape', models.CharField(max_length=200)),
                ('indices', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OnePoint',
            fields=[
                ('simulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='visualize.Simulation')),
                ('avg_slip_tr', models.FloatField()),
                ('avg_psv_tr', models.FloatField()),
                ('avg_vrup_tr', models.FloatField()),
                ('std_slip_tr', models.FloatField()),
                ('std_psv_tr', models.FloatField()),
                ('std_vrup_tr', models.FloatField()),
                ('avg_slip_sa', models.FloatField()),
                ('avg_psv_sa', models.FloatField()),
                ('avg_vrup_sa', models.FloatField()),
                ('std_slip_sa', models.FloatField()),
                ('std_psv_sa', models.FloatField()),
                ('std_vrup_sa', models.FloatField()),
                ('med_slip_sa', models.FloatField()),
                ('med_psv_sa', models.FloatField()),
                ('med_vrup_sa', models.FloatField()),
                ('mad_slip_sa', models.FloatField()),
                ('mad_psv_sa', models.FloatField()),
                ('mad_vrup_sa', models.FloatField()),
                ('med_del_tau', models.FloatField()),
                ('avg_del_tau', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Parameters',
            fields=[
                ('bc1', models.TextField()),
                ('bc2', models.TextField()),
                ('dt', models.TextField()),
                ('dx', models.TextField()),
                ('eplasticity', models.TextField()),
                ('faultnormal', models.TextField()),
                ('friction', models.TextField()),
                ('ihypo', models.TextField()),
                ('np3', models.TextField()),
                ('npml', models.TextField()),
                ('nt', models.TextField()),
                ('nn', models.TextField()),
                ('rundir', models.TextField()),
                ('pcdep', models.TextField(blank=True, null=True)),
                ('rcrit', models.TextField(blank=True, null=True)),
                ('delts', models.TextField(blank=True, null=True)),
                ('tm0', models.TextField(blank=True, null=True)),
                ('tmnucl', models.TextField(blank=True, null=True)),
                ('trelax', models.TextField(blank=True, null=True)),
                ('simulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='visualize.Simulation')),
            ],
        ),
        migrations.CreateModel(
            name='Rupture_Parameters',
            fields=[
                ('simulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='visualize.Simulation')),
                ('fault_extent', models.FloatField()),
                ('magnitude', models.FloatField()),
                ('del_tau', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='simulation',
            field=models.ManyToManyField(to='visualize.Simulation'),
        ),
        migrations.AddField(
            model_name='simulation_output',
            name='simulation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualize.Simulation'),
        ),
        migrations.AddField(
            model_name='simulation_input',
            name='simulation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualize.Simulation'),
        ),
        migrations.AddField(
            model_name='figure',
            name='simulation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visualize.Simulation'),
        ),
        migrations.AlterUniqueTogether(
            name='simulation_output',
            unique_together=set([('simulation', 'file')]),
        ),
        migrations.AlterUniqueTogether(
            name='simulation_input',
            unique_together=set([('simulation', 'field')]),
        ),
    ]
