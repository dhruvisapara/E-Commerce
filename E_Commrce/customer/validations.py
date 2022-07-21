from rest_framework import serializers

from customer.models import Business
from django.utils.translation import gettext_lazy as _


def validate_company_name(value):
    """
        This is validates that company is not already registered.
    """
    message = _("This company is already exists.")
    if Business.objects.filter(company_name=value).exists():
        raise serializers.ValidationError(message)
    return value


def validate_revenue(value):
    """
        It validates company revenue is enough for registered their business successfully.
    """
    if value < 50000:
        raise serializers.ValidationError("Your company revenue is not enough.")
    return value


def validate_id(value):
    if not Business.objects.filter(business_customer_id=value).exists():
        raise serializers.ValidationError(
            "You dont registered any company yet." "First register yor company."
        )
    return value
