# Generated by Django 4.0.5 on 2023-12-19 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_processedwoolbatch_processedbatch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shearingrequest',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producer'),
        ),
        migrations.DeleteModel(
            name='ProcessedBatch',
        ),
    ]