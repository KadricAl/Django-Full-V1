# Generated by Django 5.1.6 on 2025-05-22 10:44

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('devices', '0001_initial'),
        ('technician', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstalledDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('installation_date', models.DateField(default=django.utils.timezone.localdate)),
                ('warranty_expiry', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('installed', 'Installed'), ('deactivated', 'deactivated')], default='pending', max_length=20)),
                ('last_yearly_service_done', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device')),
                ('shop', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customer.shop')),
                ('technician', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='technician.technicianprofile')),
            ],
        ),
    ]
