# Generated by Django 3.0.4 on 2020-05-04 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0006_auto_20200420_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillfulness',
            name='skill_level',
            field=models.SmallIntegerField(default=0),
        ),
    ]