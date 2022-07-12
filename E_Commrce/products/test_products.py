from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED


BASE_URL = "/api/v1/products/"


class TestProductList:

    def test_for_unauthorized_user(self, api_client):
        """
        It should test that user is authorized or not.
        Return 401 for unauthorized user.
        """
        response = api_client.get(BASE_URL)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_for_authorized_user(self, api_client, product_creation):
        """
        It should test that user is authorized.
        """
        api_client.force_authenticate(product_creation.user)
        response = api_client.get(BASE_URL)
        assert response.status_code == HTTP_200_OK

    def test_create_product(self, api_client, product_creation, create_category):
        product_payload = {
            "name": product_creation.name,
            "price": product_creation.price,
            "brand": product_creation.brand,
            "new_price": product_creation.new_price,
            "old_price": product_creation.old_price,
            "quantity": product_creation.quantity,
            "user": product_creation.user.id,
            "is_bestseller": product_creation.is_bestseller,
            "is_featured": product_creation.is_featured,
            "created_at": product_creation.created_at,
            "updated_at": product_creation.updated_at,
            "product": create_category.id
        }
        api_client.force_authenticate(product_creation.user)
        response = api_client.post(BASE_URL, data=product_payload, format='json')
        response.json().pop('id')
        assert response.status_code == HTTP_201_CREATED
        # assert response.json() == product_payload
