# Generated by Django 5.1.4 on 2025-03-27 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_hotel_rating_count_alter_hotel_badge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='hotel_contact',
            new_name='hotel_contact_number',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='description',
            new_name='landmark',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_address',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_owner_name',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_state',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='hotel_zipcode',
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_main_img',
            field=models.ImageField(default=2, upload_to='hotel_main_image'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='hotel_more_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_owner_name', models.CharField(default=None, max_length=250)),
                ('hotel_contact', models.IntegerField(default=0)),
                ('hotel_state', models.CharField(default=None, max_length=50)),
                ('hotel_city', models.CharField(default=None, max_length=50)),
                ('hotel_zipcode', models.CharField(default=None, max_length=20)),
                ('hotel_address', models.CharField(default=None, max_length=250)),
                ('hotel_gstnumber', models.CharField(blank=True, max_length=20, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.hotel')),
            ],
        ),
    ]
