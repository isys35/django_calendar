# Generated by Django 3.2.5 on 2021-07-07 11:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_userevent_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='notification',
            field=models.DurationField(blank=True, choices=[(datetime.timedelta(seconds=3600), 'За час'), (datetime.timedelta(seconds=7200), 'За два часа'), (datetime.timedelta(seconds=14400), 'За 4 часа'), (datetime.timedelta(days=3), 'За день'), (datetime.timedelta(days=7), 'За неделю')], db_index=True, max_length=30, null=True, verbose_name='Напоминание'),
        ),
    ]
