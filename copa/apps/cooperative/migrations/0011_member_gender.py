# Generated by Django 3.0.6 on 2021-05-21 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0010_memberfield_cooperative'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'M'), ('Female', 'F')], max_length=50, null=True),
        ),
    ]
