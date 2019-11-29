# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book(models.Model):
    booid = models.IntegerField(primary_key=True, null=False)
    bookname = models.CharField(max_length=64, null=False)
    writer = models.CharField(max_length=64, null=False)
    press = models.CharField(max_length=64, null=False)
    neededcredit = models.IntegerField(default=0)