from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
)

from products.filters import ProductFilter
from products.models import Products

BASE_URL = "/api/v1/products/"
SEARCH_COUNT = 1
DELETE_COUNT = 0
PRODUCT_PAYLOAD = dict()


class TestProductList:
    def setUp(self, product_creation, create_category):
        self.product_payload = {
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
            "product": create_category.pk,
        }

        return PRODUCT_PAYLOAD.update(self.product_payload)

    def test_get_form_unauthorized_user(self, api_client):
        """
        It should test that user is authorized or not.
        Return 401 for unauthorized user.
        """
        response = api_client.get(BASE_URL)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_form_authorized_user(self, api_client, product_creation):
        """
        It should test that user is authorized.
        """
        api_client.force_authenticate(product_creation.user)
        response = api_client.get(BASE_URL)
        assert response.status_code == HTTP_200_OK

    """If pass payload data into parameter than that test case will be going to failed."""

    def test_post_form_product(self, api_client, product_creation, create_category):
        """
        It should test post API of products.
        """
        api_client.force_authenticate(product_creation.user)
        self.setUp(product_creation, create_category)
        data_count = Products.objects.all().count()
        response = api_client.post(BASE_URL, data=PRODUCT_PAYLOAD, format="json")
        final_data_count = Products.objects.all().count()
        response.json().pop("id")
        assert response.status_code == HTTP_201_CREATED
        assert final_data_count == data_count + 1

    def test_update_form_category(
        self, api_client, product_creation, create_category, staff_user
    ):
        """
        It should test update API of products.
        """
        api_client.force_authenticate(product_creation.user)
        response = api_client.put(
            "/api/v1/products/" + str(product_creation.pk) + "/",
            {
                "name": "TEST title",
                "price": 788,
                "quantity": 2,
                "old_price": 456,
                "new_price": 322,
                "is_bestseller": True,
                "is_featured": True,
                "product": [{"categories": "Test item", "description": "good luck"}],
            },
            format="json",
        )
        updated_data = response.json().get("name")
        assert response.status_code == HTTP_200_OK
        assert updated_data == "TEST title"

    def test_delete_form_product(self, product_creation, api_client):
        """
        It should test delete API for product.
        """
        api_client.force_authenticate(product_creation.user)

        response = api_client.delete(
            "/api/v1/products/" + str(product_creation.pk) + "/"
        )
        response_data_count = len(response.content)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert response_data_count == DELETE_COUNT

    def test_search_fields_for_products(self, product_creation, api_client):
        """
        It should test that search action perform according to Product model fields.
        """
        data = {"search": product_creation.name}
        api_client.force_authenticate(product_creation.user)
        response = api_client.get(BASE_URL, data)
        response_data = response.json().get("results")
        data_count = len(response_data)
        assert response.status_code == HTTP_200_OK
        assert SEARCH_COUNT == data_count

        if data_count:
            assert response_data[data_count - 1].get("name") == data.get("search")

    def test_wrong_search_for_products(self, api_client, product_creation):
        """
        It should test wrong search field for products.
        """
        data = {"search": "wrong product name"}
        api_client.force_authenticate(product_creation.user)
        response = api_client.get(BASE_URL, data)
        response_data = response.json().get("results")
        data_count = len(response_data)
        assert response.status_code == HTTP_200_OK
        assert SEARCH_COUNT != data_count
        if data_count:
            assert response_data[data_count - 1].get("name") == data.get("search")

    def test_filter_fields(self, product_creation, api_client):
        """
        It should test that filter fields are according to Product model fields.
        """
        api_client.force_authenticate(product_creation.user)
        data = {"name": product_creation.name}
        product_filter = ProductFilter(data, queryset=Products.objects.all())
        response = api_client.get(BASE_URL, data=product_filter.data)
        assert response.status_code == HTTP_200_OK
        assert product_filter.is_valid()
        assert product_filter.qs.count() == 1
