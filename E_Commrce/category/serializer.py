from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from category.models import Category
from products.serializer import ProductSerializer


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(ModelSerializer):
    sub_category = RecursiveSerializer(many=True, read_only=True)
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            "slug",
            "id",
            "category_name",
            "description",
            "parent",
            "sub_category",
            "created_at",
            "updated_at",
            "product",
        )

        extra_kwargs = {"parent": {"write_only": True}}
