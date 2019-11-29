# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-29 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('booid', models.IntegerField(primary_key=True, serialize=False)),
                ('bookname', models.CharField(max_length=64)),
                ('writer', models.CharField(max_length=64)),
                ('press', models.CharField(max_length=64)),
                ('neededcredit', models.IntegerField(default=0)),
            ],
        ),
    ]
