# Generated by Django 4.2.5 on 2023-12-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]