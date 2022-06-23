# Generated by Django 4.0.4 on 2022-06-23 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0014_alter_cartitem_product'),
        ('address', '0003_alter_address_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0020_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_address', to='address.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_order', to='cart.cart'),
        ),
        migrations.AlterField(
            model_name='points',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_point', to=settings.AUTH_USER_MODEL),
        ),
    ]
