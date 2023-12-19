# Generated by Django 4.0.5 on 2023-12-19 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0017_alter_service_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processing_details', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('processed_quantity', models.PositiveIntegerField(blank=True)),
                ('producer_delivery_address', models.TextField(blank=True, null=True)),
                ('producer_delivery_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(default='pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.batch')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.service')),
            ],
        ),
    ]