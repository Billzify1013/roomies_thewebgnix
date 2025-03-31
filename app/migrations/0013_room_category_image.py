# Generated by Django 5.1.4 on 2025-03-29 12:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_hotel_all_images_rooms_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='room_category_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_img', models.ImageField(upload_to='category_image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.room_category')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotel')),
            ],
        ),
    ]
