# Generated by Django 3.0.6 on 2021-06-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20210614_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='productivityfield',
            name='default_value',
            field=models.FloatField(default=0),
        ),
    ]