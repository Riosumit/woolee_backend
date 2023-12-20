# Generated by Django 4.0.5 on 2023-12-19 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_processedbatch_alter_batch_producers_processedstore_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_id', models.CharField(max_length=50, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=10)),
                ('location', models.CharField(default='In Farm', max_length=200)),
                ('ref', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.processor')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.store')),
            ],
        ),
    ]