# Generated by Django 4.0.4 on 2022-06-14 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_remove_points_user_point_points_order_point'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]
