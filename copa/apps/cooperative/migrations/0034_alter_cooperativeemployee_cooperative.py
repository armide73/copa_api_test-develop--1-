# Generated by Django 3.2.15 on 2022-12-05 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0033_cooperativeemployee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperativeemployee',
            name='cooperative',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cooperative.cooperative'),
        ),
    ]