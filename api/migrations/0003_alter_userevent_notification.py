# Generated by Django 3.2.5 on 2021-07-07 11:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='notification',
            field=models.DurationField(blank=True, choices=[('1HOUR', datetime.timedelta(seconds=3600)), ('2HOUR', datetime.timedelta(seconds=7200)), ('4HOUR', datetime.timedelta(seconds=14400)), ('DAY', datetime.timedelta(days=1)), ('WEEK', datetime.timedelta(days=7))], db_index=True, max_length=30, null=True, verbose_name='Напоминание'),
        ),
    ]
