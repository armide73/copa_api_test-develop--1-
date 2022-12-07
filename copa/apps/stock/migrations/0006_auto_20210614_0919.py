# Generated by Django 3.0.6 on 2021-06-14 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20210614_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productivityfield',
            name='select_options',
        ),
        migrations.AddField(
            model_name='productivityfield',
            name='field_choice',
            field=models.CharField(blank=True, choices=[('unity', 'unity'), ('francs', 'francs')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productivityfield',
            name='field_type',
            field=models.CharField(blank=True, choices=[('number', 'number')], max_length=255, null=True),
        ),
    ]