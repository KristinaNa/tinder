# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

class Photo(models.Model):
    user = models.ForeignKey(User)
    photo = models.FileField(upload_to='documents')
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.ForeignKey(User)
    photo = models.ForeignKey(Photo, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
