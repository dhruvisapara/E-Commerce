from decimal import Decimal

from django.db.models import Sum, F
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from cart.models import Cart, CartItem


class CartItemSerializer(ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_brand = serializers.CharField(source="product.brand", read_only=True)
    product_price = serializers.CharField(source="product.price", read_only=True)
    product_category = serializers.CharField(
        source="product.category.category_name", read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "product_name",
            "quantity",
            "product_brand",
            "product",
            "cart_item",
            "product_price",
            "product_category",
            "get_total_price",




        ]
        extra_kwargs = {
            "cart_item": {"write_only": True},
            "product": {"write_only": True},
        }


class CartSerializer(ModelSerializer):
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    carts = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "status", "carts"]

