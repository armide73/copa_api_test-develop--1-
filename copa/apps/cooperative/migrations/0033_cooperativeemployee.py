# Generated by Django 3.2.15 on 2022-12-05 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0032_member_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='CooperativeEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=100)),
                ('employee_id', models.CharField(max_length=100, unique=True)),
                ('address', models.TextField(blank=True)),
                ('phone_number', models.CharField(max_length=70)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.cooperative')),
            ],
        ),
    ]
