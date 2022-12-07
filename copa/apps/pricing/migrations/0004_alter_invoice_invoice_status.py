# Generated by Django 3.2.15 on 2022-11-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0003_auto_20221107_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_status',
            field=models.CharField(choices=[('paid', 'Paid'), ('unpaid', 'Unpaid'), ('pending_payment', 'Pending Payment')], default='unpaid', max_length=255),
        ),
    ]