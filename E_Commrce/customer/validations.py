from rest_framework import serializers

from customer.models import Business


def validate_company_name(value):
    if Business.objects.filter(company_name=value).exists():
        raise serializers.ValidationError("This company is already registered .")

    return value


def validate_revenue(value):
    if value < 50000:
        raise serializers.ValidationError("Your company revenue is not enough.")
    return value
