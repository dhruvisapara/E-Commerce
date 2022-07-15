from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from cart.models import Cart

BASE_URL = '/api/v1/cart/'
CART_PAYLOAD = dict()
DELETE_COUNT = 0


class TestCart:
    def test_post_form_category(self, cart_creation, api_client, cart_item_creation):
        """
        It should test that only superuser can create the category.
        """
        before_cart_count = Cart.objects.all().count()
        cart_item_payload = [
            {
                "product": cart_item_creation.product.id,
                "quantity": cart_item_creation.quantity,
            }
        ]
        cart_payload = {
            "carts": cart_item_payload,
        }
        api_client.force_authenticate(cart_creation.user)
        response = api_client.post(BASE_URL, data=cart_payload, format='json')
        after_cart_count = Cart.objects.all().count()
        assert response.status_code == HTTP_201_CREATED
        assert after_cart_count == before_cart_count + 1

    def test_delete_cart(self, api_client, cart_creation):
        api_client.force_authenticate(cart_creation.user)
        response = api_client.delete(
            BASE_URL + str(cart_creation.id) + "/"
        )
        response_data_count = len(response.content)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert response_data_count == DELETE_COUNT

    def test_update_cart(self, cart_creation, api_client):
        """
        It should test that category should update by only admin who created that category.
        """
        api_client.force_authenticate(cart_creation.user)
        cart = Cart.objects.create(number_of_items=2.0, total=43.88, text_total=43.99, text_percentage=53.00,user=cart_creation.user)

        updated_cart = {
            'number_of_items': cart_creation.number_of_items,
            'total': cart_creation.total,
            'text_total': cart_creation.text_total,
            'text_percentage': cart_creation.text_percentage,
            "carts":[

            ]

        }
        response = api_client.put(
            BASE_URL + str(cart.pk) + "/",
            data=updated_cart,
            format="json",
        )
        updated_data = response.json().get("number_of_items")
        assert response.status_code == HTTP_200_OK
        assert updated_data == cart_creation.number_of_items
