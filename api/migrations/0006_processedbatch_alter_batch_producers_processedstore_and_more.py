# Generated by Django 4.0.5 on 2023-12-19 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_shearingrequest_producer_delete_processedbatch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedBatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='processed wool', max_length=100)),
                ('raw_quantity', models.PositiveIntegerField(default=0)),
                ('processed_quantity', models.PositiveIntegerField(default=0)),
                ('qr_code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('production_date', models.DateField(auto_now_add=True)),
                ('cleanliness', models.DecimalField(decimal_places=2, max_digits=5)),
                ('texture', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='batch',
            name='producers',
            field=models.ManyToManyField(blank=True, null=True, to='api.producer'),
        ),
        migrations.CreateModel(
            name='ProcessedStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity_available', models.PositiveIntegerField(default=0)),
                ('processedbatch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.processedbatch')),
                ('processor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.processor')),
            ],
        ),
        migrations.AddField(
            model_name='processedbatch',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.batch'),
        ),
        migrations.AddField(
            model_name='processedbatch',
            name='processor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.processor'),
        ),
    ]
