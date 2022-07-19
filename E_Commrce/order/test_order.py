from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


BASE_URL = "/api/v1/orders/"


class TestOrder:
    def test_order(self, api_client, cart_creation, address_creation):
        """It should test that order is created for right cart that is not used before."""
        api_client.force_authenticate(cart_creation.user)
        data = {
            "cart": cart_creation,
            "address": address_creation.pk
        }
        response = api_client.post(BASE_URL, data)
        assert response.status_code == HTTP_201_CREATED

    def test_wrong_order(self, api_client, order_creation, address_creation):
        """It should test that order is created for wrong cart which is already used."""
        api_client.force_authenticate(order_creation.user)
        data = {
            "cart": order_creation.cart,
            "address": address_creation.pk
        }
        response = api_client.post(BASE_URL, data)
        assert response.status_code == HTTP_400_BAD_REQUEST
