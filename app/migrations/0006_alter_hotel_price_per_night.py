# Generated by Django 5.1.4 on 2025-03-27 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_hotel_contact_hotel_hotel_contact_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='price_per_night',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
