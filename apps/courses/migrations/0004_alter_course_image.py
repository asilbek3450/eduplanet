# Generated by Django 4.2.7 on 2024-06-03 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_videocontent_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]
