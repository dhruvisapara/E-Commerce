from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from customer.models import Customer, Business
from customer.validations import validate_company_name, validate_revenue
from pdb import set_trace as pdb


class CustomerSerializer(ModelSerializer):
    """Customer registration serializer."""

    is_staff = True
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Customer.objects.all())],
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
        """
        It should validate that both passwords are same.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        """
        It should convert password into hashed format.
        """
        user = Customer.objects.create(
            email=validated_data["email"], username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class BusinessUserSerializer(ModelSerializer):
    company_name = serializers.CharField(validators=[validate_company_name])
    revenue = serializers.IntegerField(validators=[validate_revenue])

    class Meta:
        model = Business
        fields = "__all__"

    def create(self, validated_data):
        """
            It should create current user as business user.
        """
        validated_data["business_customer"] = self.context["request"].user
        return Business.objects.create(**validated_data)


class StaffMembersSerializer(ModelSerializer):
    staff_members = CustomerSerializer(many=True)
    id = serializers.IntegerField(required=False)
    company_name = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True)

    class Meta:

        model = Customer
        fields = ["id", "staff_members", "company_name", "username"]

    def validate(self, data):
        """
        It should validate that manager must register least one company
        """

        if not Business.objects.filter(business_customer_id=data["id"]).exists():
            raise serializers.ValidationError(
                "You dont registered any company yet." "First register yor company."
            )
        return data

    def create(self, validated_data):
        """
            Now manager add multiple staff members using writable nested serializer.
            For generated staff members parent will be manager(current user)
        """
        staff_members = validated_data.pop("staff_members")
        manager = super(StaffMembersSerializer, self).create(validated_data)

        for staff_member in staff_members:
            staff_member["manager"] = manager.id
            staff_serializer = CustomerSerializer(data=staff_member)
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()

        return manager

    def update(self, instance, validated_data):
        """
        manager can create and update and destroy staff members.
        """
        staff_members = validated_data.pop("staff_members")
        instance = super(StaffMembersSerializer, self).update(instance, validated_data)

        for staff_member in staff_members:

            if "id" in staff_member:

                if Customer.objects.filter(id=staff_member["id"]).exists():
                    staff = Customer.objects.get(id=staff_member["id"])
                    staff.username = staff_member.get("username", staff.username)
                    staff.email = staff_member.get("email", staff.description)
                    staff.first_name = staff_member.get("first_name", staff.first_name)
                    staff.last_name = staff_member.get("last_name", staff.last_name)
                    staff.birth_date = staff_member.get("birth_date", staff.birth_date)
                    staff.address = staff_member.get("address", staff.address)
                    staff.gender = staff_member.get("gender", staff.gender)
                    staff.phone_number = staff_member.get(
                        "phone_number", staff.phone_number
                    )
                    staff.age = staff_member.get("age", staff.age)
                    staff.password = staff_member.get("password", staff.password)
                    staff.password2 = staff_member.get("password2", staff.password2)

                    staff.save()

                else:
                    continue

            else:

                staff_member.pop("password2")
                staff = Customer.objects.create(**staff_member, manager=instance)
                staff.is_staff = True
                staff.set_password(staff_member["password"])
                staff.save()

        return instance

    def get_company_name(self, obj):
        user = Business.objects.filter(business_customer=obj.manager.id)
        serializer = BusinessUserSerializer(instance=user, many=True)
        return serializer.data
