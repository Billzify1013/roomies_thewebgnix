# Generated by Django 5.1.4 on 2025-03-28 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_hotel_aminities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='hotel',
        ),
        migrations.CreateModel(
            name='Room_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=300, null=True)),
                ('category_code', models.CharField(blank=True, max_length=300, null=True)),
                ('category_badge', models.CharField(blank=True, max_length=50, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotel')),
            ],
        ),
        migrations.AddField(
            model_name='hotel_all_images',
            name='rooms_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.room_category'),
        ),
        migrations.DeleteModel(
            name='HotelImage',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
