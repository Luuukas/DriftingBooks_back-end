# Generated by Django 2.2.7 on 2019-12-01 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='coverurl',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(max_length=512),
        ),
    ]
