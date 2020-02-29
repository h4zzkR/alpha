# Generated by Django 2.2.7 on 2020-02-29 10:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200224_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 10, 32, 9, 809340, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 10, 32, 9, 808377, tzinfo=utc)),
        ),
    ]
