from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_create_category(create_category, api_client):
    """
        It should test that only superuser can create the category.
    """
    response = api_client.post('http://127.0.0.1:8000/api/v1/category/', json=create_category)
    assert response.status_code, status.HTTP_201_CREATED


def test_for_staff(staff_user, api_client):
    """
    It should return success code for staff user.
    """
    api_client.force_authenticate(staff_user)
    response = api_client.get('http://127.0.0.1:8000/api/v1/category/')
    assert response.status_code == HTTP_200_OK


def test_for_non_staff(non_staff_user, api_client):
    """
    It should give status code for non_staff user
    """
    api_client.force_authenticate(non_staff_user)
    response = api_client.get('http://127.0.0.1:8000/api/v1/category/')
    assert response.status_code == HTTP_403_FORBIDDEN


def test_check_any_matching_category(create_category, api_client,create_sub_category):
    """
    It should test that any existing category is there.
    """

    assert create_category != create_sub_category
