# Generated by Django 3.0.4 on 2020-04-06 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='previous_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]