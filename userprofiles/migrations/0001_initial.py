# Generated by Django 3.0.4 on 2020-03-20 00:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('skills', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skillfulness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.DecimalField(decimal_places=3, default=0, max_digits=4)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_skillfulness', to='skills.Skill')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('CS', 'Current Student'), ('CR', 'Career Related'), ('MI', 'Mathematics Instructor'), ('SS', 'Self Study')], default='SS', max_length=2)),
                ('test_date', models.DateField(blank=True, null=True)),
                ('skills', models.ManyToManyField(through='userprofiles.Skillfulness', to='skills.Skill')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='skillfulness',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_skillfulness', to='userprofiles.UserProfile'),
        ),
    ]
