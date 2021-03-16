# Generated by Django 3.1.7 on 2021-03-15 20:06

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import lottery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('pool', models.JSONField(default=lottery.models.generate_result_pool, verbose_name='result pool')),
                ('results', models.JSONField(blank=True, default=list, verbose_name='results')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
                ('picks', models.JSONField(default=lottery.models.generate_random_picks)),
                ('draw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='lottery.draw', verbose_name='draw')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
