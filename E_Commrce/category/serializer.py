from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from category.models import Category


# class SuperSubCategory(serializers.ModelSerializer):
#     product = ProductSerializer(many=True)
#
#     class Meta:
#         model = Category
#         fields = ("category_name", "product")
#
#     def create(self, validated_data):
#         product = validated_data("product")
#         category = Category.objects.create(**validated_data)
#         for categories in product:
#             Products.objects.create(category=category, **categories)
#             return category


class SubCategorySerializer(serializers.ModelSerializer):
    # sub_category = SuperSubCategory(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ("id", "categories", "description", "parent")


class CategorySerializer(ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ("id", "categories", "sub_categories", "description", "user")

    def validate(self, attrs):
        if "user" != 1:
            raise serializers.ValidationError("Only super admin can add category .")

    def create(self, validated_data):

        sub_categories = validated_data.pop("sub_categories")
        validated_data["user"] = self.context["request"].user
        parent = super(CategorySerializer, self).create(validated_data)

        for sub_category in sub_categories:
            sub_category["parent"] = parent.id
            sub_cat_serializer = SubCategorySerializer(data=sub_category)
            sub_cat_serializer.is_valid(raise_exception=True)
            sub_cat_serializer.save()

        return parent

    # def create(self, validated_data):
    #     sub_categories = validated_data.pop("sub_categories")
    #     parent = Category.objects.create(**validated_data)
    #     for sub_category in sub_categories:
    #         Category.objects.create(parent=parent, **sub_category)
    #     return parent

    def update(self, instance, validated_data):

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
