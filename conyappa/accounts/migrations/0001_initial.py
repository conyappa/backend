# Generated by Django 3.1.7 on 2021-03-15 20:06

import uuid

import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models

import accounts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last updated at')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('rut', models.PositiveIntegerField(default=None, null=True, unique=True, verbose_name='RUT')),
                ('check_digit', models.PositiveSmallIntegerField(default=None, null=True, verbose_name='RUT check digit')),
                ('balance', models.PositiveIntegerField(default=0, verbose_name='balance')),
                ('winnings', models.PositiveIntegerField(default=0, verbose_name='winnings')),
                ('extra_tickets_ttl', models.JSONField(blank=True, default=accounts.models.generate_initial_extra_tickets_ttl, verbose_name='extra tickets TTL')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['rut'], name='accounts_us_rut_a2654b_idx'),
        ),
    ]
