# Generated by Django 3.0.1 on 2019-12-21 12:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_auto_20191221_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='useremailconfirmation',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 22, 12, 39, 49, 130356, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userpasswordrecovery',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 22, 12, 39, 49, 130356, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]