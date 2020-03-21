# Generated by Django 3.0.4 on 2020-03-21 01:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('start_skills', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('end_skills', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('units', models.ManyToManyField(related_name='curricula', to='units.Unit')),
            ],
            options={
                'verbose_name_plural': 'curricula',
            },
        ),
    ]
