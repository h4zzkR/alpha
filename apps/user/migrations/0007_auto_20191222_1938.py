# Generated by Django 2.2.7 on 2019-12-22 16:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20191217_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 23, 16, 38, 59, 81426, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 23, 16, 38, 59, 81426, tzinfo=utc)),
        ),
    ]