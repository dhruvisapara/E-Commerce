# Generated by Django 4.0.4 on 2022-06-22 08:40

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_rename_nature_of_buisness_business_nature_of_business'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='business',
            managers=[
                ('company_list', django.db.models.manager.Manager()),
            ],
        ),
    ]
