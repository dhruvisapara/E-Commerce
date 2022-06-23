# Generated by Django 4.0.4 on 2022-06-23 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='area',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='address',
            name='block',
            field=models.CharField(default=None, max_length=5),
        ),
        migrations.AddField(
            model_name='address',
            name='building_name',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='address',
            name='flat_number',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='address',
            name='floor',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.CharField(default=1, max_length=20),
        ),
    ]
