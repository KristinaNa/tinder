# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.FileField(upload_to=b'static'),
        ),
    ]
