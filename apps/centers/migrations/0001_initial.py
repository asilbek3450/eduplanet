# Generated by Django 4.2.7 on 2024-01-09 15:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

operations = [
    migrations.CreateModel(
        name='Category',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=128)),
            ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
        ],
    ),
    migrations.CreateModel(
        name='LearningCenter',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=128)),
            ('description', models.TextField()),
            ('location', models.CharField(max_length=128)),
            ('email', models.EmailField(max_length=254)),
            ('phone_number', models.CharField(max_length=17, unique=True, validators=[
                django.core.validators.RegexValidator('^\\+998\\d{9,15}$',
                                                      message='Phone number must be in the format +998XXXXXXXXX, where X is a digit.')])),
            ('image', models.ImageField(upload_to='learning_center_images/')),
            ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('categories', models.ManyToManyField(to='centers.category')),
        ],
    ),
]
