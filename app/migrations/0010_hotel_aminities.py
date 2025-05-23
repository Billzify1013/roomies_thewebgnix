# Generated by Django 5.1.4 on 2025-03-28 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_hotel_all_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='hotel_aminities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aminities_name', models.CharField(blank=True, max_length=250, null=None)),
                ('icon_code', models.CharField(blank=True, max_length=250, null=None)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotel')),
            ],
        ),
    ]
