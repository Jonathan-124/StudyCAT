# Generated by Django 3.0.4 on 2020-05-04 16:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0005_auto_20200504_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='end_skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='unit',
            name='start_skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
    ]
