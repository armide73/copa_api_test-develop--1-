# Generated by Django 3.2.15 on 2022-11-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spenn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spennsession',
            name='access_token',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='spennsession',
            name='refresh_token',
            field=models.TextField(blank=True, null=True),
        ),
    ]
