# Generated by Django 3.2.9 on 2021-12-06 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_alter_driver_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 6, 21, 58, 11, 368370)),
        ),
    ]
