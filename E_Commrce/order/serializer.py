from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from address.serializer import AddressSerializer
from cart.serializer import CartSerializer
from order.models import Order, Points


class OrderSerializer(ModelSerializer):
    cart_user = serializers.CharField(source="user.username", read_only=True)
    items = serializers.IntegerField(source="cart.get_total_items", read_only=True)
    price = serializers.IntegerField(source="cart.get_total_cost", read_only=True)
    points = serializers.SerializerMethodField()

    def get_points(self, obj):
        points = Points.objects.filter(user=obj.user).first()
        points_collection = points.points_gained if points else "Sorry there is no points in your account."
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
            "total_cost"
        ]
        extra_kwargs = {'user': {'write_only': True}, }

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return Order.objects.create(**validated_data)

    def validate(self, data):
        """
        cart use as reference for order only once.
        """
        if Order.objects.filter(cart_id=data["cart"]).exists():
            raise serializers.ValidationError(
                "This cart is already ordered."
            )
        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cart'] = CartSerializer(instance.cart).data
        response['address'] = AddressSerializer(instance.address).data
        return response
