# Generated by Django 3.2.6 on 2021-09-15 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0024_remove_member_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='identity_card',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
