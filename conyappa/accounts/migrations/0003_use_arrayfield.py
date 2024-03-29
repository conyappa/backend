# Generated by Django 3.1.7 on 2021-03-27 15:28

import django.contrib.postgres.fields
from django.db import migrations, models

import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='extra_tickets_ttl',
        ),
        migrations.AddField(
            model_name='user',
            name='extra_tickets_ttl',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(), blank=True, default=accounts.models.generate_initial_extra_tickets_ttl, size=None, verbose_name='extra tickets TTL'),
        ),
    ]
