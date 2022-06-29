from rest_framework import serializers
from customer.models import Business
from pdb import set_trace as pdb


def validate_company_name(value):
    """
        This is validates that company is not already registered.
    """
    if Business.objects.filter(company_name=value).exists():
        raise serializers.ValidationError("This company is already registered .")

    return value


def validate_revenue(value):
    """
        It validates company revenue is enough for registered their business successfully.
    """
    if value < 50000:
        raise serializers.ValidationError("Your company revenue is not enough.")
    return value
