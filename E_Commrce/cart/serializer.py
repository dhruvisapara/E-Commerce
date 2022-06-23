from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from cart.models import Cart, CartItem


class CartItemSerializer(ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_brand = serializers.CharField(source="product.brand", read_only=True)
    product_price = serializers.CharField(source="product.price", read_only=True)
    category_name = serializers.CharField(
        source="product.category.name", read_only=True
    )
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_name",
            "quantity",
            "product_brand",
            "product",
            "product_price",
            "category_name",
            "get_total_price",
        ]
        extra_kwargs = {
            "cart_item": {"write_only": True},
            "product": {"write_only": True},
        }


class CartSerializer(ModelSerializer):
    carts = CartItemSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Cart
        fields = [

            "id",
            "carts",
            "get_total_cost",
            "get_total_items",
        ]

    def validate_get_total_price(value):
        if value < 1000:
            raise serializers.ValidationError(
                "your order amount is less then 999 so you have to pay delivery charges."
                "Do you really want to continue.")

    def create(self, validated_data):

        carts = validated_data.pop("carts")
        validated_data["user"] = self.context["request"].user
        cart = Cart.objects.create(**validated_data)

        for item in carts:
            CartItem.objects.create(cart_item=cart, **item)
        return cart

    def update(self, instance, validated_data):
        carts = validated_data.pop("carts")
        instance = super(CartSerializer, self).update(instance, validated_data)
        for cart_items in carts:

            if "id" in cart_items:

                if CartItem.objects.filter(id=cart_items["id"]).exists():
                    item = CartItem.objects.get(id=cart_items["id"])
                    item.product = cart_items.get("product", item.product)
                    item.quantity = cart_items.get("quantity", item.quantity)
                    item.save()
                else:
                    continue
            else:
                item = CartItem.objects.create(**cart_items, cart_item=instance)
                # sub_cat = super(CategorySerializer, self).create(validated_data)
                item.save()

        return instance
