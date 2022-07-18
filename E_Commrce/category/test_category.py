import json
from typing import Union
import pytest
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
VALIDATION_URL='/api/v1/category_validation/'
SEARCH_COUNT = 1
DELETE_COUNT = 0


class TestCategoryCreation:
    def test_post_form_category(self, create_category, create_sub_category, api_client):
        """
        It should test that only superuser can create the category.
        """
        before_category_count = Category.objects.all().count()
        sub_categoey_payload = [
            {
                "categories": create_sub_category.categories,
                "description": create_sub_category.description,
                "parent": create_category.id,
            }
        ]
        category_payload = {
            "categories": create_category.categories,
            "description": create_category.description,
            "sub_categories": sub_categoey_payload,
        }
        api_client.force_authenticate(create_category.user)
        response = api_client.post(BASE_URL1, data=category_payload)
        after_category_count = Category.objects.all().count()
        assert response.status_code == HTTP_201_CREATED
        assert after_category_count == before_category_count + 1

    def test_update_form_category(self, create_category, api_client):
        """
        It should test that category should update by only admin who created that category.
        """
        api_client.force_authenticate(create_category.user)
        category = Category.objects.create(categories="CLOTH", description="ABCD")

        updated_category = {
            "categories": "Topwear",
            "description": "ABCD",
            "sub_categories": [
                {
                    "categories": "tunic",
                    "description": "ghjk",
                }
            ],
        }
        response = api_client.put(
            "/api/v1/category/" + str(category.pk) + "/",
            data=updated_category,
            format="json",
        )
        updated_data = response.json().get("categories")
        assert response.status_code == HTTP_200_OK
        assert updated_data == "Topwear"

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

    def test_get_form_display_all_content(self, api_client, create_category):
        api_client.force_authenticate(create_category.user)
        response = api_client.get(BASE_URL1 + "?page_size=all")
        category_count = Category.objects.all().count()
        assert HTTP_200_OK == response.status_code
        assert category_count > 1

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


class TestCategoryValidation:
    def test_post_form_validation(self, api_client, staff_user):
        api_client.force_authenticate(staff_user)
        category_creation = Category.objects.create(categories="CLOTH", description="ABCD")
        payload_data = {
            "categories": category_creation.categories,
            "description": "ABCD",
            "sub_categories": [
                {
                    "categories": "tunic",
                    "description": "ghjk",
                },
            ]
        }
        response=api_client.post(VALIDATION_URL,data=payload_data)
        validation_error=response.json().get('categories')[0]
        sub_string=' already existed.'
        assert sub_string in validation_error
