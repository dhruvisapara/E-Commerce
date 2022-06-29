from rest_framework.serializers import ModelSerializer

from address.models import Address
from pdb import set_trace as pdb


class AddressSerializer(ModelSerializer):
    """
        This serializer is for creating address.
    """
    class Meta:
        model = Address
        fields = [
            "id",
            "user_address",
            "phone",
            "email",
            "name",
            "block",
            "building_name",
            "floor",
            "flat_number",
            "street",
            "area",
            "full_address",
        ]

    def create(self, validated_data):
        """
            It should create current user .
        """
        validated_data["user_address"] = self.context["request"].user
        return Address.objects.create(**validated_data)
