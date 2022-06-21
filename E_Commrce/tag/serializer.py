from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from category.models import Category
from category.serializer import CategorySerializer
from products.models import Products
from products.serializer import ProductSerializer
from tag.models import TaggedItem


class TagSerializer(ModelSerializer):
    category_tag_types = serializers.SerializerMethodField()
    product_tag_type = serializers.SerializerMethodField()

    class Meta:
        model = TaggedItem
        fields = "__all__"

    def get_category_tag_types(self, instance):

        tag_types = list(Category.objects.filter(id=instance.object_id).values())
        serializer = CategorySerializer(data=tag_types, many=True)
        return serializer.initial_data

    def get_product_tag_type(self, instance):
        tag_types = list(Products.objects.filter(id=instance.object_id).values())
        serializer = ProductSerializer(data=tag_types, many=True)
        return serializer.initial_data

