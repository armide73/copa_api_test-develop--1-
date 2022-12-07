# Generated by Django 3.0.6 on 2021-04-24 14:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cooperative', '0004_auto_20210424_1209'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CooperativeFields',
            new_name='CooperativeField',
        ),
        migrations.AlterModelOptions(
            name='cooperative',
            options={'verbose_name_plural': 'Cooperatives'},
        ),
        migrations.AlterModelOptions(
            name='cooperativefield',
            options={'verbose_name_plural': 'CooperativeFields'},
        ),
        migrations.AlterModelOptions(
            name='cooperativemeta',
            options={'verbose_name_plural': 'CooperativeMeta'},
        ),
    ]
