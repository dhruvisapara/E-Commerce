from collections import OrderedDict

import stripe
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from address.serializers import AddressSerializer
from cart.serializers import CartSerializer
from order.models import Order, Points

stripe.api_key = "sk_test_51LE9ZESCeFbdDABQ3olyTyP7elkIVCNZJJHjy9YPwR3SRlxddCjD8ENbK3ndjKAsGhOOz1IdqlatFoj9gLkZpjR000m3oy61ZT "


class OrderSerializer(ModelSerializer):
    cart_user = serializers.CharField(source="user.username", read_only=True)
    items = serializers.IntegerField(source="cart.get_total_items", read_only=True)
    price = serializers.IntegerField(source="cart.get_total_cost", read_only=True)
    token = serializers.CharField(source='settings.STRIPE_SECRET_KEY', read_only=True)
    points = serializers.SerializerMethodField()

    def get_points(self, obj):
        """
            This method should display current user points and if no points are there then give error message.
        """
        points = Points.objects.filter(user=obj.user).first()
        points_collection = (
            points.points_gained
            if points
            else "Sorry there is no points in your account."
        )
        return points_collection

    class Meta:
        model = Order
        fields = [
            "id",
            "cart_user",
            "address",
            "cart",
            "status",
            "price",
            "tax",
            "estimated_delivery_charges",
            "items",
            "points",
            "user",
            "total_cost",
            "token",
        ]
        extra_kwargs = {
            "user": {"write_only": True},
        }

    def create(self, validated_data) -> Order:
        """
            It creates payment intent using stripe PaymentIntent for particular orders.
        """
        validated_data["user"] = self.context["request"].user
        product = Order.objects.create(**validated_data)
        response = stripe.PaymentIntent.create(
            amount=product.total_cost,
            currency="usd",
            payment_method_types=["card"]
        )
        print(response)
        return product

    def validate(self, data) -> dict:
        """
            cart use as reference for order only once.
        """
        if Order.objects.filter(cart_id=data["cart"]).exists():
            raise serializers.ValidationError("This cart is already ordered.")
        return data

    def to_representation(self, instance) -> OrderedDict:
        """
            To represent cart and address more elaborately.
        """
        response = super().to_representation(instance)
        response['cart'] = CartSerializer(instance.cart).data
        response['address'] = AddressSerializer(instance.address).data
        return response
