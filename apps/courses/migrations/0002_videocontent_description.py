# Generated by Django 4.2.7 on 2024-01-10 04:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocontent',
            name='description',
            field=models.TextField(default=datetime.datetime(2024, 1, 10, 4, 8, 9, 487986, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]