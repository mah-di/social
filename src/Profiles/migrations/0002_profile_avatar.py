# Generated by Django 3.2.5 on 2021-07-26 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar.png', upload_to='avatar/'),
        ),
    ]
