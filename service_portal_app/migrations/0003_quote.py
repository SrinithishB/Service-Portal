# Generated by Django 5.1.5 on 2025-01-23 16:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_portal_app', '0002_alter_servicerequest_location'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('quote_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_quotes', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='service_portal_app.servicerequest')),
            ],
            options={
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
                'ordering': ['-created_at'],
            },
        ),
    ]
