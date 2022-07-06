import pytest
from pytest_factoryboy import register
from django.test import TestCase
from category.factories import CategoryFactory
from customer.models import Customer
from rest_framework.test import APIClient

register(CategoryFactory)


@pytest.mark.django_db
def test_staff_member_active(active_user: Customer):
    assert active_user.is_staff == True


@pytest.mark.django_db
def test_negetive_user(inactivate_user: Customer):
    assert inactivate_user.is_staff == False


# def test_unauthorized_request(api_client):
#     import pdb;
#     pdb.set_trace()
#     url = reverse('http://127.0.0.1:8000/api/v1/category/')
#
#     response = api_client.get(url)
#     assert response.status_code == 401
#     assert response.customer.is_staff == True


class MyTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate()
        user = Customer.objects.create_user(username='TestUser', email='test@test.test', password='testpass',
                                            is_staff=True)
        self.client.force_authenticate(user)

    def test_failing_for_non_staff(self):
        if self.client:
            self.client.get('/category/')

    def test_for_activate_staff(self):
        import pdb;
        pdb.set_trace()
