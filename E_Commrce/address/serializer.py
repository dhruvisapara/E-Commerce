from rest_framework.serializers import ModelSerializer

from address.models import Address


class AddressSerializer(ModelSerializer):
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
        validated_data["user_address"] = self.context["request"].user
        return Address.objects.create(**validated_data)
