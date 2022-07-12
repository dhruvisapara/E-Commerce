import json
from typing import Union

from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT

from category.filters import Searchfilter
from category.models import Category
from category.serializers import CategorySerializer
from category.views import CategoryView

url = '/api/v1/category/'
url1 = '/api/v2/category/'

class TestCategoryCreation:

    def test_create_category(self, create_category, create_sub_category, api_client):
        """
        It should test that only superuser can create the category.
        """

        sub_categoey_payload = [{
            "categories": create_sub_category.categories,
            "description": create_sub_category.description,
            "parent": create_category.id,
        }]

        category_payload = {
            "categories": create_category.categories,
            "description": create_category.description,
            "sub_categories": sub_categoey_payload
        }
        api_client.force_authenticate(create_category.user)
        response = api_client.post(url, data=category_payload)
        assert response.status_code == HTTP_201_CREATED

    def test_update_category(self, create_category, api_client):
        """
        It should test that category should update by only admin who created that category.
        """
        api_client.force_authenticate(create_category.user)
        category = Category.objects.create(categories="CLOTH", description="ABCD")
        updated_category = {
            'categories': "Topwear",
            'description': "ABCD"
        }
        response = api_client.put(
            '/api/v1/category/'+str(create_category.id)+"/",
            data=updated_category,
            content_type='application/json'
        )
        assert response.status_code == HTTP_400_BAD_REQUEST
    def test_delete_category(self,create_category,api_client):
        api_client.force_authenticate(create_category.user)
        data={
            'categories':create_category.categories,
            "description":create_category.description
        }
        response = api_client.delete(
            '/api/v1/category/'+str(create_category.id)+"/",
            data=data,
            content_type='application/json'
        )
        assert response.status_code == HTTP_204_NO_CONTENT

class TestCategoryList:

    def test_for_staff(self, api_client, staff_user):
        """
        It should return success code for staff user.
        """
        api_client.force_authenticate(staff_user)
        response = api_client.get(url)
        assert response.status_code == HTTP_200_OK

    def test_for_non_staff(self, non_staff_user, api_client):
        """
        It should give status code for non_staff user
        """
        api_client.force_authenticate(non_staff_user)
        response = api_client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_check_any_matching_category(self, create_category, create_sub_category):
        """
        It should test that any existing category is there.
        """
        assert create_category.categories != create_sub_category.categories

    def test_version_of_url(self,api_client,create_category,create_sub_category):
        """
        It should display data according to the entered versions .
        """
        data1={
            "categories":create_category.categories,
            "description":create_category.description
        }
        data2={
            "categories":create_sub_category.categories,
            "description":create_sub_category.description
        }
        api_client.force_authenticate(create_category.user)
        api_client.force_authenticate(create_sub_category.user)

        response=api_client.get(url,data=data1)
        response2=api_client.get(url1,data=data2)

        assert response.status_code == HTTP_200_OK
        assert response2.status_code == HTTP_200_OK

class TestSearchFilterCategory:
    def test_search_fields(self, api_client, create_category):
        """
        It should test that search field is in the range of model field.
        """
        data = {
            'categories': create_category.categories
        }
        api_client.force_authenticate(create_category.user)
        response = api_client.get(url, data)
        response_data=response.json().get('result').get('results')
        data_count=len(response_data)
        assert  response.status_code== HTTP_200_OK
        assert len(data)== data_count

        if data_count:
            assert response_data[data_count-1].get('categories')== data.get("categories")


    def test_wrong_search(self, api_client, create_category):
        """
        It should test wrong search field for category.
        """
        data={
            'search': "wrong category name"
        }
        api_client.force_authenticate(create_category.user)
        response = api_client.get(url, data)
        response_data = response.json().get('result').get('results')
        data_count = len(response_data)
        assert response.status_code == HTTP_200_OK
        assert len(data) != data_count
        if data_count:
            assert response_data[data_count - 1].get('categories') == data.get("categories")

    def test_filter_category(self,create_category,api_client):
        """
        It should test that category will filters by correct field.
        """
        api_client.force_authenticate(create_category.user)
        data={
            "categories":create_category.categories
        }
        challenge_filter = Searchfilter(data, queryset=Category.objects.all())
        response = api_client.get(url,data= challenge_filter.data)
        assert response.status_code == HTTP_200_OK
        assert challenge_filter.is_valid()
        assert challenge_filter.qs.count() == 1