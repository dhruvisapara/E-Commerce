from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from order.models import Order, Points


class OrderSerializer(ModelSerializer):
    cart_user = serializers.CharField(source="user.username", read_only=True)
    address = serializers.CharField(source="user.address", read_only=True)
    phone = serializers.CharField(source="user.phone_number", read_only=True)
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
            "cart",
            "status",
            "price",
            "items",
            "address",
            "phone",
            "points",
            "user",

        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return Order.objects.create(**validated_data)
