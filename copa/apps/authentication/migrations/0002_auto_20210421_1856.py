# Generated by Django 3.0.6 on 2021-04-21 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='names',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]