# Generated by Django 2.2.7 on 2020-01-19 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborator',
            name='role',
            field=models.CharField(blank=True, default='Not specified', max_length=30),
        ),
    ]
