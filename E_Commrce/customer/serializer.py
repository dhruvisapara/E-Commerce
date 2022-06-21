from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from customer.models import Customer, Business


class CustomerSerializer(ModelSerializer):
    """Customer ragistration serializer."""

    is_staff = True
    email = serializers.EmailField(
        # Each customer has unique email id
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
            "full_name",
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
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        # user.set_password(validated_data["password"])
        user.save()
        return user


class BusinessUserSerializer(ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"

    def create(self, validated_data):
        validated_data["business_customer"] = self.context["request"].user
        return Business.objects.create(**validated_data)

    def validate(self, data):
        if data['revenue'] < 50000:
            raise serializers.ValidationError('Your company revenue is not enough .')
        return data


class StaffMembersSerializer(ModelSerializer):
    staff_members = CustomerSerializer(many=True)
    id = serializers.IntegerField(required=False)

    class Meta:

        model = Customer
        fields = ['id', 'staff_members']

    def validate_id(self, data):
        business_id = Business.objects.order_by('business_customer')
        if data["id"] not in business_id:
            raise serializers.ValidationError('You dont registerd any company yet.')
        return data

    def create(self, validated_data):
        staff_members = validated_data.pop("staff_members")
        manager = super(StaffMembersSerializer, self).create(validated_data)
        for staff_member in staff_members:
            staff_member["manager"] = manager.id
            staff_serializer = CustomerSerializer(data=staff_member)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()

        return manager

    def update(self, instance, validated_data):

        staff_members = validated_data.pop("staff_members")
        instance = super(StaffMembersSerializer, self).update(instance, validated_data)

        for staff_member in staff_members:

            if "id" in staff_member:

                if Customer.objects.filter(id=staff_member["id"]).exists():
                    staff = Customer.objects.get(id=staff_member["id"])
                    staff.username = staff_member.get("username", staff.username)
                    staff.email = staff_member.get(
                        "email", staff.description
                    )
                    staff.first_name = staff_member.get("first_name", staff.first_name)
                    staff.last_name = staff_member.get("last_name", staff.last_name)
                    staff.birth_date = staff_member.get("birth_date", staff.birth_date)
                    staff.address = staff_member.get("address", staff.address)
                    staff.gender = staff_member.get("gender", staff.gender)
                    staff.phone_number = staff_member.get("phone_number", staff.phone_number)
                    staff.age = staff_member.get("age", staff.age)
                    staff.password = staff_member.get("password", staff.password)
                    staff.password2 = staff_member.get("password2", staff.password2)

                    staff.save()

                else:
                    continue

            else:

                staff_member.pop("password2")
                staff = Customer.objects.create(**staff_member, manager=instance)
                staff.set_password(staff_member['password'])
                staff.save()

        return instance
