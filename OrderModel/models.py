from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class Order(models.Model):
    oid = models.CharField(max_length=64, primary_key=True)
    uid = models.IntegerField(null=False, default=-1)
    otype = models.IntegerField()
    expresscompany = models.IntegerField(default=-1)
    trackingnumber = models.CharField(max_length=64, default="")
    botid = models.IntegerField()
    address = models.CharField(max_length=256)
    name = models.CharField(max_length=64)
    phonenumber = models.CharField(max_length=32)
    state = models.IntegerField()
    submittime = models.DateTimeField(default=timezone.now)
    completetime = models.DateTimeField(default=timezone.now)