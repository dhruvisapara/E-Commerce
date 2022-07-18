from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from cart.models import Cart, CartItem

BASE_URL = "/api/v1/cart/"
BASE_URL1 = "/api/v1/cart_item/"
CART_PAYLOAD = dict()
DELETE_COUNT = 0


class TestCart:
    def test_get_form_empty_cart_count(self, api_client, db):
        response = api_client.get(BASE_URL)
        sub_string = "empty"
        message = response.json().get('message')
        assert sub_string in message

    def test_get_form_cart(self, api_client, cart_creation):
        api_client.force_authenticate(cart_creation.user)
        response = api_client.get(BASE_URL)
        sub_string = "success"
        message = response.json().get('message')
        assert sub_string in message

    def test_post_form_cart(self, cart_creation, api_client, cart_item_creation):
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
        response = api_client.post(BASE_URL, data=cart_payload, format="json")
        after_cart_count = Cart.objects.all().count()
        assert response.status_code == HTTP_201_CREATED
        assert after_cart_count == before_cart_count + 1

    def test_delete_cart(self, api_client, cart_creation):
        api_client.force_authenticate(cart_creation.user)
        response = api_client.delete(BASE_URL + str(cart_creation.pk) + "/")
        response_data_count = len(response.content)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert response_data_count == DELETE_COUNT

    def test_update_cart(self, cart_creation, api_client, product_creation, cart_item_creation, update_cart_item):
        """
        It should test that category should update by only admin who created that category.
        """
        api_client.force_authenticate(cart_creation.user)

        cart_item_payload = [
            {
                "product": cart_item_creation.product.id,
                "quantity": cart_item_creation.quantity,
            }
        ]
        cart_payload = {
            "carts": cart_item_payload,
        }
        response = api_client.post(BASE_URL, data=cart_payload, format="json")
        pk = response.json().get('id')
        updated_cart_item_payload = [
            {
                "product": update_cart_item.product.id,
                "quantity": update_cart_item.quantity,
            }
        ]
        updated_cart = {
            "carts": updated_cart_item_payload
        }
        update_response = api_client.put(
            BASE_URL + str(pk) + "/",
            data=updated_cart
        )

        import pdb
        pdb.set_trace()
        assert response.status_code == HTTP_201_CREATED
        assert update_response == HTTP_200_OK



class TestCartUser:
    def setUp(self, cart_creation):
        self.updated_cart = {
            "number_of_items": cart_creation.number_of_items,
            "total": cart_creation.total,
            "text_total": cart_creation.text_total,
            "text_percentage": cart_creation.text_percentage,
            "carts": [],
        }
        return CART_PAYLOAD.update(self.updated_cart)

    def test_get_form_math_cart_user_to_request_user(self, api_client, cart_creation):
        """
        It should test that business user and request user is same.
        """
        self.setUp(cart_creation)
        api_client.force_authenticate(cart_creation.user)
        response = api_client.get(BASE_URL, data=CART_PAYLOAD, format="json")
        cart_user = response.json().get("result").get("results")[0]["user"]
        assert response.status_code == HTTP_200_OK
        assert cart_user == cart_creation.user.id

    def test_get_form_cart_items(self, api_client, cart_creation):
        api_client.force_authenticate(cart_creation.user)
        response = api_client.get(BASE_URL1)
        sub_string = "success"
        message = response.json().get('message')
        assert sub_string in message
