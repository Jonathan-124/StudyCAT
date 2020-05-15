# Generated by Django 3.0.4 on 2020-05-14 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20200426_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonbugreport',
            name='reason',
            field=models.CharField(choices=[('FI', 'There is something factually incorrect with the lesson'), ('TI', 'There are typos present in the lesson'), ('DI', 'The lesson is not displaying correctly'), ('SI', 'There are knowledge gaps between this lesson and previous/subsequent lessons'), ('OT', 'Other')], max_length=2),
        ),
        migrations.AlterField(
            model_name='questionbugreport',
            name='reason',
            field=models.CharField(choices=[('PI', 'There is something wrong with the question prompt'), ('PC', 'My answer deserves partial credit (please write down your answer)'), ('AI', 'There is something wrong with the answer(s)'), ('DI', 'The question is not displaying correctly'), ('OT', 'Other')], max_length=2),
        ),
    ]