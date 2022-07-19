import json
from typing import Union

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from category.filters import Searchfilter
from category.models import Category
from category.serializers import CategorySerializer
from category.views import CategoryView

BASE_URL1 = "/api/v1/category/"
BASE_URL2 = "/api/v2/category/"
SEARCH_COUNT = 1
DELETE_COUNT = 0


class TestCategoryCreation:
    def test_post_form_category(self, create_category, create_sub_category, api_client):
        """
        It should test that only superuser can create the category.
        """
        api_client.force_authenticate(create_category.user)
        before_category_count = Category.objects.all().count()
        sub_categoey_payload = [
            {
                "categories": create_sub_category.categories,
                "description": create_sub_category.description,
                "parent": create_category.user.id,
            }
        ]
        category_payload = {
            "categories": create_category.categories,
            "description": create_category.description,
            "sub_categories": sub_categoey_payload,
        }
        response = api_client.post(BASE_URL1, data=category_payload, format='json')
        after_category_count = Category.objects.all().count()
        assert response.status_code == HTTP_201_CREATED
        assert after_category_count > before_category_count

    def test_update_category(self, create_category, create_sub_category, updated_fixture,api_client ):
        api_client.force_authenticate(create_category.user)

        sub_category_payload = [
            {
                "categories": create_sub_category.categories,
                "description": create_sub_category.description,
            }
        ]
        catgory_payload = {
            "categories": create_category.categories,
            "description": create_category.description,
            "sub_categories": sub_category_payload
        }
        response = api_client.post(BASE_URL1, data=catgory_payload, format="json")
        pk = response.json().get('id')
        sub_category_pk = response.json().get('sub_categories')[0]['id']
        updated_sub_category_payload = [
            {
                "id": sub_category_pk,
                "categories": updated_fixture.categories,
                "description": updated_fixture.description,
            }

        ]
        updated_category = {
            "categories": "Tops",
            "description": "czvcvxvx",
            "sub_categories": [{
                "id": updated_sub_category_payload[0]['id'],
                "categories": updated_sub_category_payload[0]['categories'],
                "description": updated_sub_category_payload[0]['description'],
            },
                {
                    "categories": "sewdwewvwv",
                    "description": "wdvwsvwv",

                }
            ]
        }

        update_response = api_client.put(
            BASE_URL1 + str(pk) + "/",
            data=updated_category, format='json'
        )
        update_check=update_response.json().get('categories')

        assert response.status_code == HTTP_201_CREATED
        assert update_response.status_code == HTTP_200_OK
        assert update_check == "Tops"


    def test_delete_form_category(self, create_category, api_client):
        api_client.force_authenticate(create_category.user)
        response = api_client.delete(
            "/api/v1/category/" + str(create_category.id) + "/"
        )
        response_data_count = len(response.content)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert response_data_count == DELETE_COUNT


class TestCategoryList:
    def test_get_form_unauthorized_user(self, api_client):
        """
        It should test that user is authorized or not.
        Return 401 for unauthorized user.
        """
        response = api_client.get(BASE_URL1)
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_get_form_authorized_user(self, api_client, create_category):
        """
        It should test that user is authorized.
        """
        api_client.force_authenticate(create_category.user)
        response = api_client.get(BASE_URL1)
        assert response.status_code == HTTP_200_OK

    def test_get_form_staff_user(self, api_client, staff_user):
        """
        It should return success code for staff user.
        """
        api_client.force_authenticate(staff_user)
        response = api_client.get(BASE_URL1)
        assert response.status_code == HTTP_200_OK

    def test_get_form_non_staff_user(self, non_staff_user, api_client):
        """
        It should give status code for non_staff user
        """
        api_client.force_authenticate(non_staff_user)
        response = api_client.get(BASE_URL1)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_check_any_matching_category(self, create_category, create_sub_category):
        """
        It should test that any existing category is there.
        """
        assert create_category.categories != create_sub_category.categories

    def test_version_of_url(self, api_client, create_category, create_sub_category):
        """
        It should display data according to the entered versions .
        """
        data1 = {
            "categories": create_category.categories,
            "description": create_category.description,
        }
        data2 = {
            "categories": create_sub_category.categories,
            "description": create_sub_category.description,
        }
        api_client.force_authenticate(create_category.user)
        api_client.force_authenticate(create_sub_category.user)

        response = api_client.get(BASE_URL1, data=data1)
        response2 = api_client.get(BASE_URL2, data=data2)

        assert response.status_code == HTTP_200_OK
        assert response2.status_code == HTTP_200_OK

    def test_get_form_display_all_content(self, api_client, create_category):
        api_client.force_authenticate(create_category.user)
        response = api_client.get(BASE_URL1+"?page_size=all")
        category_count=Category.objects.all().count()
        assert HTTP_200_OK == response.status_code
        assert category_count > 1

class TestSearchFilterCategory:
    def test_search_fields_for_category(self, api_client, create_category):
        """
        It should test that search field is in the range of model field.
        """
        data = {"categories": create_category.categories}
        api_client.force_authenticate(create_category.user)
        response = api_client.get(BASE_URL1, data)
        response_data = response.json().get("result").get("results")
        data_count = len(response_data)
        assert response.status_code == HTTP_200_OK
        assert SEARCH_COUNT == data_count

        if data_count:
            assert response_data[data_count - 1].get("categories") == data.get(
                "categories"
            )

    def test_get_form_wrong_search_for_category(self, api_client, create_category):
        """
        It should test wrong search field for category.
        """
        data = {"search": "wrong category name"}
        api_client.force_authenticate(create_category.user)
        response = api_client.get(BASE_URL1, data)
        response_data = response.json().get("result").get("results")
        data_count = len(response_data)
        assert response.status_code == HTTP_200_OK
        assert SEARCH_COUNT != data_count
        if data_count:
            assert response_data[data_count - 1].get("categories") == data.get(
                "categories"
            )

    def test_filter_fields_for_category(self, create_category, api_client):
        """
        It should test that category will filters by correct field.
        """
        api_client.force_authenticate(create_category.user)
        data = {"categories": create_category.categories}
        category_filter = Searchfilter(data, queryset=Category.objects.filter(id=2))
        response = api_client.get(BASE_URL1, data=category_filter.data)
        assert response.status_code == HTTP_200_OK
        assert category_filter.is_valid()
        assert category_filter.qs.count() == 1


