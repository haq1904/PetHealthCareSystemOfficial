# Generated by Django 5.1.4 on 2025-02-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_cage_capacity_alter_customer_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]
