# Generated by Django 3.2.9 on 2021-12-11 21:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0005_auto_20211211_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 11, 21, 39, 13, 715070)),
        ),
    ]
