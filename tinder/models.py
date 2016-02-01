# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class auth_user(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class upload_foto(models.Model):
    user_id = models.IntegerField()
    #foto = models.CharField(max_length=30)
    foto = models.FileField(upload_to='documents')

class rating(models.Model):
    user_id = models.IntegerField()
    foto_id = models.IntegerField()