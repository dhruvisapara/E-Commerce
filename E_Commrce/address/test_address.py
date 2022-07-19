from django.test import TestCase

# Create your tests here.
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.utils import json
from urllib3 import encode_multipart_formdata

from address.models import Address

BASE_URL = '/api/v1/address/'


class TestAddress:
    def test_post_form_address(self, api_client, address_creation):
        api_client.force_authenticate(address_creation.user_address)
        before_count = Address.objects.all().count()
        data = {
            "user_address": address_creation.user_address.pk,
            "email": address_creation.email,
            "name": address_creation.name,
            "building_name": address_creation.building_name,
            "block": '234',
            "floor": address_creation.floor,
            "flat_number": '123',
            "street": address_creation.street,
            "area": address_creation.area
        }

        response = api_client.post(BASE_URL, data)
        after_count = Address.objects.all().count()
        assert response.status_code == HTTP_201_CREATED
        assert after_count == before_count + 1

    def test_get_form_address(self, api_client, address_creation):
        api_client.force_authenticate(address_creation.user_address)
        response = api_client.get(BASE_URL)
        assert response.status_code == HTTP_200_OK
