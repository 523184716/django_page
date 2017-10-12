# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import  models
from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=256)
    IP = models.GenericIPAddressField()

class Page(models.Model):
    per_item = models.CharField(max_length=50)