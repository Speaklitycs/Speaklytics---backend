# Generated by Django 5.1.3 on 2025-01-23 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_ticketmodel_errormodel_is_finished_errormodel_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='errormodel',
            name='progress',
            field=models.FloatField(default=0.0),
        ),
    ]
