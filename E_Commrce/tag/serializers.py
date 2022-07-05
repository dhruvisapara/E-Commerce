from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from category.models import Category
from category.serializers import CategorySerializer
from products.models import Products
from products.serializers import ProductSerializer
from tag.models import TaggedItem


class TagSerializer(ModelSerializer):
    content_types = serializers.CharField(source="content_type.name")
    category_tag_types = serializers.SerializerMethodField()
    product_tag_type = serializers.SerializerMethodField()

    class Meta:
        model = TaggedItem
        fields = "__all__"

    def get_category_tag_types(self, instance) -> CategorySerializer:
        """
            It should display category for tags if tag is related to category.
        """
        tag_types = list(Category.objects.filter(id=instance.object_id).values())
        serializer = CategorySerializer(data=tag_types, many=True)
        return serializer.initial_data

    def get_product_tag_type(self, instance) -> ProductSerializer:
        """
            It should display product for tags if tag is related to products.
        """
        tag_types = list(Products.objects.filter(id=instance.object_id).values())
        serializer = ProductSerializer(data=tag_types, many=True)
        return serializer.initial_data
