# Generated by Django 2.2.7 on 2019-11-26 17:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20191126_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 27, 17, 30, 3, 129653, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 27, 17, 30, 3, 129653, tzinfo=utc)),
        ),
    ]