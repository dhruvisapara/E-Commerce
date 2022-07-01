from django.core.validators import EMPTY_VALUES
from rest_framework import serializers
from rest_framework.serializers import ListSerializer, ModelSerializer

from products.models import Products


class ProductListSerializer(ListSerializer):

    def create(self, validated_data) -> Products:
        """
            It should create multiple products at a time in list.
        """
        product = [Products(**item) for item in validated_data]
        bulk_product = Products.objects.bulk_create(product)
        return bulk_product

    def update(self, instance, validated_data) -> list:
        """
            to update list data .
        """
        products = []
        for data in validated_data:
            if "id" in data and EMPTY_VALUES:
                Products.objects.filter(id=data["id"]).update(**data)
                products.append(data)
            else:
                products.append(Products.objects.create(**data))
        return products


class ProductSerializer(ModelSerializer):
    """
        This serializer is for product related stuff.
    """
    id = serializers.IntegerField(required=False)
    brand = serializers.CharField(read_only=True)

    class Meta:
        model = Products
        list_serializer_class = ProductListSerializer
        fields = [
            "id",
            "name",
            "price",
            "brand",
            "quantity",
            "old_price",
            "new_price",
            "is_bestseller",
            "is_featured",
            "created_at",
            "updated_at",
            "user",
        ]

    # def validate_name(self, value):
    #     """
    #     Check that user's registered company name and this name will same
    #     """
    #     if self.us not in value.lower():
    #         raise serializers.ValidationError("Blog post is not about Django")
    #     return value
