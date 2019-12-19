# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    phonenumber = models.CharField(unique=True, max_length=20, null=False)
    address = models.CharField(max_length=1024)
    credit = models.IntegerField(default=0)
    enrolldatetime = models.DateTimeField(null=False)