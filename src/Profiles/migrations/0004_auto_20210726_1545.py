# Generated by Django 3.2.5 on 2021-07-26 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_friendship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received', to='Profiles.profile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent', to='Profiles.profile'),
        ),
    ]