# Generated by Django 3.2.5 on 2021-07-27 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0007_rename_postlike_like'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]