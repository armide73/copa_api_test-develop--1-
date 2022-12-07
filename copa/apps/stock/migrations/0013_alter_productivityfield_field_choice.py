# Generated by Django 3.2.6 on 2021-09-17 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0012_alter_productivity_unity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productivityfield',
            name='field_choice',
            field=models.CharField(blank=True, choices=[('percentage', 'percentage'), ('francs', 'francs'), ('francsadd', 'francsadd'), ('francsremove', 'francsremove'), ('none', 'none'), ('', '')], default='none', max_length=255, null=True),
        ),
    ]
