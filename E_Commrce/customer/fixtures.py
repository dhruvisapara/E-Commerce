import pytest

from customer.factories import CustomerFactory
from customer.models import Customer
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory


@pytest.fixture
def staff_user(db) -> Customer:
    """It creates user A for test purposes."""
    return Customer.objects.create_user(username="active-user", is_staff=True, password="staff1234##",
                                        is_superuser=True)


@pytest.fixture
def non_staff_user(db) -> Customer:
    """It creates user A for test purposes."""
    return Customer.objects.create_user(username="inactive", password="nonstaff1234##")


@pytest.fixture
def api_client():
    return APIClient()
@pytest.fixture
def api_factory():
    return APIRequestFactory()

@pytest.fixture
def authenticate_user(db):
    request = CustomerFactory.create()
    return request
