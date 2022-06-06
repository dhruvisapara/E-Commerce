from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from customer.models import Customer


class CustomerSerializer(ModelSerializer):
    """Each customer has unique email id"""

    is_staff = True
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Customer.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "birth_date",
            "address",
            "gender",
            "phone_number",
            "age",
            "password",
            "password2",
            "is_staff",
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        """passwords should be same."""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        """It should convert password into hashed format."""
        user = Customer.objects.create(
            email=validated_data["email"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
