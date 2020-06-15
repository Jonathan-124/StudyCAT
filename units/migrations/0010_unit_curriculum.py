# Generated by Django 3.0.4 on 2020-06-14 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curricula', '0005_remove_curriculum_units'),
        ('units', '0009_auto_20200613_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='curriculum',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='units', to='curricula.Curriculum'),
        ),
    ]