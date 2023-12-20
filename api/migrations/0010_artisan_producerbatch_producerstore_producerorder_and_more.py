# Generated by Django 4.0.5 on 2023-12-20 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0009_service_remove_processedbatch_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artisan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artisan_name', models.CharField(max_length=100)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('pincode', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('experience_years', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProducerBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='raw wool', max_length=100)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('qr_code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=5)),
                ('color', models.CharField(max_length=50)),
                ('softness', models.CharField(max_length=50)),
                ('production_date', models.DateField(auto_now_add=True)),
                ('quality_certificate_link', models.URLField(blank=True, null=True)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producer')),
            ],
        ),
        migrations.CreateModel(
            name='ProducerStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('batch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.producerbatch')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producer')),
            ],
        ),
        migrations.CreateModel(
            name='ProducerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_id', models.CharField(max_length=50, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=10)),
                ('location', models.CharField(default='In Farm', max_length=200)),
                ('ref', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artisan')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producerstore')),
            ],
        ),
        migrations.CreateModel(
            name='FabricStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('desc', models.CharField(max_length=255)),
                ('qr_code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('posted_on', models.DateField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity_available', models.PositiveIntegerField(default=1)),
                ('artisian', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('processedbatch', models.ManyToManyField(blank=True, to='api.processedbatch')),
                ('producerbatch', models.ManyToManyField(blank=True, to='api.producerbatch')),
            ],
        ),
        migrations.AlterField(
            model_name='processedorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.artisan'),
        ),
    ]
