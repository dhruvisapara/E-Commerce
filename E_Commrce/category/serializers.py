from rest_framework import serializers
from rest_framework.serializers import (HyperlinkedModelSerializer,
                                        ModelSerializer)

from category.models import Category
from products.serializers import ProductSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ("id", "categories", "description", "parent")


class CategorySerializer(ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)
    id = serializers.IntegerField(required=False)
    product = ProductSerializer(read_only=True,many=True)

    class Meta:
        model = Category
        fields = ("id", "categories", "product", "sub_categories", "description", "user")

    # def validate(self, attrs):
    #     """
    #         It validates that category should create by superuser only.
    #     """
    #     import pdb ; pdb.set_trace()
    #     if "user" != 1:
    #         raise serializers.ValidationError("Only super admin can add category .")

    def create(self, validated_data) -> Category:
        """
            This should create subcategories with categories using writable nested serializer.
        """
        sub_categories = validated_data.pop("sub_categories")
        validated_data["user"] = self.context["request"].user
        parent = super(CategorySerializer, self).create(validated_data)

        for sub_category in sub_categories:
            sub_category["parent"] = parent.id
            sub_cat_serializer = SubCategorySerializer(data=sub_category)
            sub_cat_serializer.is_valid(raise_exception=True)
            sub_cat_serializer.save()

        return parent

    def update(self, instance, validated_data) -> Category:
        """
            This should update existing categories,subcategories and add new subcategories at a time.
        """
        sub_categories = validated_data.pop("sub_categories")
        instance = super(CategorySerializer, self).update(instance, validated_data)
        for sub_category in sub_categories:

            if "id" in sub_category:

                if Category.objects.filter(id=sub_category["id"]).exists():
                    sub_cat = Category.objects.get(id=sub_category["id"])
                    sub_cat.categories = sub_category.get("categories", sub_cat.categories)
                    sub_cat.description = sub_category.get(
                        "description", sub_cat.description
                    )
                    sub_cat.save()
                else:
                    continue

            else:
                sub_cat = Category.objects.create(**sub_category, parent=instance)
                # sub_cat = super(CategorySerializer, self).create(validated_data)
                sub_cat.save()

        return instance


class CatSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "url", "categories"]
