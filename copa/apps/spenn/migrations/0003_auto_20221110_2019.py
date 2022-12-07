# Generated by Django 3.2.15 on 2022-11-10 20:19

import copa.utils.app_utils.generators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spenn', '0002_auto_20221110_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='spennrequeststatus',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spennrequeststatus',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='spennsession',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spennsession',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='spennrequeststatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='spennrequeststatus',
            name='id',
            field=models.CharField(default=copa.utils.app_utils.generators.id_generater, editable=False, max_length=9, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='spennrequeststatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='spennsession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='spennsession',
            name='id',
            field=models.CharField(default=copa.utils.app_utils.generators.id_generater, editable=False, max_length=9, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='spennsession',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
