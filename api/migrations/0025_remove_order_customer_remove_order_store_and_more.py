# Generated by Django 4.0.5 on 2023-12-19 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_batch_producer_alter_store_producer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='store',
        ),
        migrations.RemoveField(
            model_name='processor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='producer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='service',
            name='user',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='producer',
        ),
        migrations.RemoveField(
            model_name='servicerequest',
            name='service',
        ),
        migrations.RemoveField(
            model_name='store',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='store',
            name='producer',
        ),
        migrations.DeleteModel(
            name='Batch',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Processor',
        ),
        migrations.DeleteModel(
            name='Producer',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='ServiceRequest',
        ),
        migrations.DeleteModel(
            name='Store',
        ),
    ]
