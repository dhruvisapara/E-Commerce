# Generated by Django 4.0.4 on 2022-05-30 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
