# Generated by Django 3.1.7 on 2021-03-15 20:06

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
                ('fintoc_data', models.JSONField(verbose_name='Fintoc object')),
                ('fintoc_id', models.CharField(max_length=32, unique=True, verbose_name='Fintoc ID')),
                ('fintoc_post_date', models.DateField(verbose_name='Fintoc post date')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movements', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'ordering': ['-fintoc_post_date'],
            },
        ),
        migrations.AddIndex(
            model_name='movement',
            index=models.Index(fields=['fintoc_id'], name='banking_mov_fintoc__171387_idx'),
        ),
    ]
