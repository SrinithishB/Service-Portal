# Generated by Django 5.1.5 on 2025-01-23 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_portal_app', '0003_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='availability_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
