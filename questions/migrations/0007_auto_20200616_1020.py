# Generated by Django 3.0.4 on 2020-06-16 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_question_permitted_symbols'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('MC', 'Multiple Choice'), ('MS', 'Multiple Selection'), ('IC', 'Image Choice'), ('NI', 'Numerical Input'), ('FI', 'Function Input'), ('MI', 'Matrix Input'), ('II', 'Interval Input')], max_length=2),
        ),
    ]
