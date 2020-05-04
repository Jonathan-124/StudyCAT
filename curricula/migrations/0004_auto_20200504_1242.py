# Generated by Django 3.0.4 on 2020-05-04 16:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0003_auto_20200504_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='end_skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='start_skills',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
    ]
