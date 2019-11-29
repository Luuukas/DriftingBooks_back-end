# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class Bottle(models.Model):
    botid = models.IntegerField(primary_key=True, null=False)
    bookname = models.CharField(max_length=64, null=False)
    writer = models.CharField(max_length=64, null=False)
    press = models.CharField(max_length=64, null=False)
    description = models.CharField(max_length=128)
    photos = models.CharField(max_length=516)
    timeouthandle = models.BooleanField()
    sendto = models.IntegerField()     # 赠送对象，0：未给个人，<0：已确定机构代号, >0:已给个人uid
    uploaddatetime = models.DateTimeField(null=False)
    state = models.IntegerField(default=0)     # 个人查看的状态, 1：未入库 2：已入库 3：已拒收 4：已捐赠