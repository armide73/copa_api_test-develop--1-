# Generated by Django 3.2.15 on 2022-11-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0005_auto_20221111_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
