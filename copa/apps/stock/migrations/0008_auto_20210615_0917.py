# Generated by Django 3.0.6 on 2021-06-15 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_productivityfield_default_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productivitymeta',
            name='prod_type',
        ),
        migrations.AlterField(
            model_name='productivityfield',
            name='field_choice',
            field=models.CharField(blank=True, choices=[('percentage', 'percentage'), ('francs', 'francs')], max_length=255, null=True),
        ),
    ]
