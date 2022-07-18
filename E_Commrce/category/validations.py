from rest_framework import serializers

from category.models import Category


def validate_categories(value):
    """
        This should validate that category is not already registered.
    """
    if Category.objects.filter(categories=value).exists():
        raise serializers.ValidationError("This category is already existed.")

    # return value
