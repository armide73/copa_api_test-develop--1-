# Generated by Django 3.0.6 on 2021-06-14 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20210614_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productivityfield',
            name='key',
            field=models.CharField(max_length=255),
        ),
    ]