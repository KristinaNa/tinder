# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0002_rating'),
    ]

    operations = [

        migrations.AddField("rating", "created_at", models.DateTimeField(auto_now_add=True)),
        migrations.AddField("upload_foto", "created_at", models.DateTimeField(auto_now_add=True))

    ]