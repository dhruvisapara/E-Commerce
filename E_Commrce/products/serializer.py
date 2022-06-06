from rest_framework.serializers import ModelSerializer
from products.models import Products


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "name",
            "price",
            "brand",
            "old_price",
            "new_price",
            "status",
            "is_bestseller",
            "is_featured",
            "quantity",
            "category",
        ]
