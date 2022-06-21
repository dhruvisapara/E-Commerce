# Generated by Django 4.0.4 on 2022-06-14 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_products_options_remove_products_is_active_and_more'),
        ('cart', '0013_alter_cartitem_cart_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='products.products'),
        ),
    ]
