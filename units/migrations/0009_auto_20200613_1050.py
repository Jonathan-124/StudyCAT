# Generated by Django 3.0.4 on 2020-06-13 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0008_auto_20200528_1846'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['precedence']},
        ),
        migrations.RenameField(
            model_name='unit',
            old_name='topological_average',
            new_name='precedence',
        ),
    ]