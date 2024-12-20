# Generated by Django 3.0.4 on 2020-04-22 10:02

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0004_skilledge_same_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='ancestor_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='skill',
            name='descendant_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, null=True, size=None),
        ),
    ]
