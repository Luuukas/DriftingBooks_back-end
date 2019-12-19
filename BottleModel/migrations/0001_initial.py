# Generated by Django 2.2.7 on 2019-12-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bottle',
            fields=[
                ('botid', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.IntegerField()),
                ('bookname', models.CharField(max_length=64)),
                ('writer', models.CharField(max_length=64)),
                ('press', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128)),
                ('photos', models.CharField(max_length=516)),
                ('timeouthandle', models.BooleanField()),
                ('sendto', models.IntegerField()),
                ('uploaddatetime', models.DateTimeField()),
                ('state', models.IntegerField(default=0)),
            ],
        ),
    ]
