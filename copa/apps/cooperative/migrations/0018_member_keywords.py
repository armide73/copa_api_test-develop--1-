# Generated by Django 3.0.6 on 2021-09-08 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0017_auto_20210908_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]