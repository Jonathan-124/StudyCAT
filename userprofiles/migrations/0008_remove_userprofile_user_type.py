# Generated by Django 3.0.4 on 2020-05-14 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0007_auto_20200504_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_type',
        ),
    ]