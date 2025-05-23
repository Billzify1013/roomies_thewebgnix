# Generated by Django 5.1.4 on 2025-03-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='available_rooms',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='total_rooms',
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_contact',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_owner_name',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='hotel',
            name='is_block',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hotel',
            name='is_verify',
            field=models.BooleanField(default=False),
        ),
    ]
