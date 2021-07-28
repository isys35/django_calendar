# Generated by Django 3.2.5 on 2021-07-28 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210727_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(db_index=True, max_length=40),
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
                ('date', models.DateTimeField()),
                ('countries', models.ManyToManyField(related_name='holidays', to='api.Country')),
            ],
        ),
    ]
