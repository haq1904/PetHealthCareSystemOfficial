# Generated by Django 5.1.4 on 2025-02-18 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_cagestatus_dirty'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CageStatus',
        ),
    ]
